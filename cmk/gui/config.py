#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import sys
import errno
import os
import copy
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from pathlib import Path

from livestatus import SiteId, SiteConfiguration, SiteConfigurations

import cmk.utils.version as cmk_version
from cmk.utils.site import omd_site, url_prefix
import cmk.utils.tags
import cmk.utils.paths
import cmk.utils.store as store

from cmk.gui.globals import user
import cmk.gui.utils as utils
import cmk.gui.i18n
from cmk.gui.i18n import _
import cmk.gui.log as log
from cmk.gui.exceptions import MKConfigError

# Kept for compatibility with pre 1.6 GUI plugins
from cmk.gui.permissions import declare_permission, declare_permission_section  # noqa: F401 # pylint: disable=unused-import

import cmk.gui.plugins.config

# This import is added for static analysis tools like pylint to make them
# know about all shipped config options. The default config options are
# later handled with the default_config dict and _load_default_config()
from cmk.gui.plugins.config.base import *  # pylint: disable=wildcard-import,unused-wildcard-import

if not cmk_version.is_raw_edition():
    from cmk.gui.cee.plugins.config.cee import *  # pylint: disable=wildcard-import,unused-wildcard-import,no-name-in-module

if cmk_version.is_managed_edition():
    from cmk.gui.cme.plugins.config.cme import *  # pylint: disable=wildcard-import,unused-wildcard-import,no-name-in-module

#   .--Declarations--------------------------------------------------------.
#   |       ____            _                 _   _                        |
#   |      |  _ \  ___  ___| | __ _ _ __ __ _| |_(_) ___  _ __  ___        |
#   |      | | | |/ _ \/ __| |/ _` | '__/ _` | __| |/ _ \| '_ \/ __|       |
#   |      | |_| |  __/ (__| | (_| | | | (_| | |_| | (_) | | | \__ \       |
#   |      |____/ \___|\___|_|\__,_|_|  \__,_|\__|_|\___/|_| |_|___/       |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |  Declarations of global variables and constants                      |
#   '----------------------------------------------------------------------'

multisite_users = {}
admin_users = []
tags = cmk.utils.tags.TagConfig()

# hard coded in various permissions
builtin_role_ids = ["user", "admin", "guest"]

# Base directory of dynamic configuration
config_dir = cmk.utils.paths.var_dir + "/web"

config_storage_format = "standard"  # new in 2.1. Possible also: "raw"


def get_storage_format() -> 'store.StorageFormat':
    return store.StorageFormat.from_str(config_storage_format)


#.
#   .--Functions-----------------------------------------------------------.
#   |             _____                 _   _                              |
#   |            |  ___|   _ _ __   ___| |_(_) ___  _ __  ___              |
#   |            | |_ | | | | '_ \ / __| __| |/ _ \| '_ \/ __|             |
#   |            |  _|| |_| | | | | (__| |_| | (_) | | | \__ \             |
#   |            |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/             |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |  Helper functions for config parsing, login, etc.                    |
#   '----------------------------------------------------------------------'


def initialize() -> None:
    load_config()
    log.set_log_levels(log_levels)
    cmk.gui.i18n.set_user_localizations(user_localizations)


def _load_config_file_to(path: str, raw_config: Dict[str, Any]) -> None:
    """Load the given GUI configuration file"""
    try:
        with Path(path).open("rb") as f:
            exec(f.read(), {}, raw_config)
    except IOError as e:
        if e.errno != errno.ENOENT:  # No such file or directory
            raise
    except Exception as e:
        raise MKConfigError(_("Cannot read configuration file %s: %s:") % (path, e))


# Load multisite.mk and all files in multisite.d/. This will happen
# for *each* HTTP request.
# FIXME: Optimize this to cache the config etc. until either the config files or plugins
# have changed. We could make this being cached for multiple requests just like the
# plugins of other modules. This may save significant time in case of small requests like
# the graph ajax page or similar.
def load_config() -> None:
    # Set default values for all user-changable configuration settings
    raw_config = get_default_config()

    # Initialize sites with default site configuration. Need to do it here to
    # override possibly deleted sites
    raw_config["sites"] = default_single_site_configuration()

    # Load assorted experimental parameters if any
    experimental_config = cmk.utils.paths.make_experimental_config_file()
    if experimental_config.exists():
        _load_config_file_to(str(experimental_config), raw_config)

    # First load main file
    _load_config_file_to(cmk.utils.paths.default_config_dir + "/multisite.mk", raw_config)

    # Load also recursively all files below multisite.d
    conf_dir = cmk.utils.paths.default_config_dir + "/multisite.d"
    filelist = []
    if os.path.isdir(conf_dir):
        for root, _directories, files in os.walk(conf_dir):
            for filename in files:
                if filename.endswith(".mk"):
                    filelist.append(root + "/" + filename)

    filelist.sort()
    for p in filelist:
        _load_config_file_to(p, raw_config)

    raw_config["sites"] = prepare_raw_site_config(raw_config["sites"])

    _prepare_tag_config(raw_config)

    # Make sure, builtin roles are present, even if not modified and saved with WATO.
    for br in builtin_role_ids:
        raw_config["roles"].setdefault(br, {})

    # TODO: Keep this until all call sites are refactored to use the ConfigContext
    # object from cmk.gui.globals, which will be introduced soon.
    globals().update(raw_config)

    execute_post_config_load_hooks()


def _prepare_tag_config(raw_config: Dict[str, Any]) -> None:
    # When the user config does not contain "tags" a pre 1.6 config is loaded. Convert
    # the wato_host_tags and wato_aux_tags to the new structure
    tag_config = raw_config["wato_tags"]
    if not any(tag_config.values()) and (raw_config["wato_host_tags"] or
                                         raw_config["wato_aux_tags"]):
        tag_config = cmk.utils.tags.transform_pre_16_tags(raw_config["wato_host_tags"],
                                                          raw_config["wato_aux_tags"])

    raw_config["tags"] = cmk.utils.tags.get_effective_tag_config(tag_config)


def execute_post_config_load_hooks() -> None:
    for func in _post_config_load_hooks:
        func()


_post_config_load_hooks: List[Callable[[], None]] = []


def register_post_config_load_hook(func: Callable[[], None]) -> None:
    _post_config_load_hooks.append(func)


def get_default_config() -> Dict[str, Any]:
    default_config = _get_default_config_from_legacy_plugins()
    default_config.update(_get_default_config_from_module_plugins())
    return default_config


def _get_default_config_from_legacy_plugins() -> Dict[str, Any]:
    default_config: Dict[str, Any] = {}
    utils.load_web_plugins("config", default_config)
    return default_config


def _get_default_config_from_module_plugins() -> Dict[str, Any]:
    config_plugin_vars: Dict = {}
    for module in _config_plugin_modules():
        config_plugin_vars.update(module.__dict__)

    default_config: Dict[str, Any] = {}
    for k, v in config_plugin_vars.items():
        if k[0] == "_":
            continue

        if isinstance(v, (dict, list)):
            v = copy.deepcopy(v)

        default_config[k] = v
    return default_config


def _config_plugin_modules() -> List[ModuleType]:
    return [
        module for name, module in sys.modules.items()
        if (name.startswith("cmk.gui.plugins.config.") or name.startswith(
            "cmk.gui.cee.plugins.config.") or name.startswith("cmk.gui.cme.plugins.config.")) and
        module is not None
    ]


def prepare_raw_site_config(site_config: SiteConfigurations) -> SiteConfigurations:
    if not site_config:
        # Prevent problem when user has deleted all sites from his
        # configuration and sites is {}. We assume a default single site
        # configuration in that case.
        return default_single_site_configuration()
    return _migrate_old_site_config(site_config)


def _migrate_old_site_config(site_config: SiteConfigurations) -> SiteConfigurations:
    for site_id, site_cfg in site_config.items():
        # Until 1.6 "replication" could be not present or
        # set to "" instead of None
        if site_cfg.get("replication", "") == "":
            site_cfg["replication"] = None

        # Until 1.6 "url_prefix" was an optional attribute
        if "url_prefix" not in site_cfg:
            site_cfg["url_prefix"] = "/%s/" % site_id

        site_cfg.setdefault("proxy", None)

        _migrate_pre_16_socket_config(site_cfg)

    return site_config


# During development of the 1.6 version the site configuration has been cleaned up in several ways:
# 1. The "socket" attribute could be "disabled" to disable a site connection. This has already been
#    deprecated long time ago and was not configurable in WATO. This has now been superseded by
#    the dedicated "disabled" attribute.
# 2. The "socket" attribute was optional. A not present socket meant "connect to local unix" socket.
#    This is now replaced with a value like this ("local", None) to reflect the generic
#    CascadingDropdown() data structure of "(type, attributes)".
# 3. The "socket" attribute was stored in the livestatus.py socketurl encoded format, at least when
#    livestatus proxy was not used. This is now stored in the CascadingDropdown() native format and
#    converted here to the correct format.
# 4. When the livestatus proxy was enabled for a site, the settings were stored in the "socket"
#    attribute. The proxy settings were an additional dict which also held a "socket" key containing
#    the final socket connection properties.
#    This has now been split up. The top level socket settings are now used independent of the proxy.
#    The proxy options are stored in the separate key "proxy" which is a mandatory key.
def _migrate_pre_16_socket_config(site_cfg: Dict[str, Any]) -> None:
    socket = site_cfg.get("socket")
    if socket is None:
        site_cfg["socket"] = ("local", None)
        return

    if isinstance(socket, tuple) and socket[0] == "proxy":
        site_cfg["proxy"] = socket[1]

        # "socket" of proxy could either be None or two element tuple for "tcp"
        proxy_socket = site_cfg["proxy"].pop("socket", None)
        if proxy_socket is None:
            site_cfg["socket"] = ("local", None)

        elif isinstance(socket, tuple):
            site_cfg["socket"] = ("tcp", {
                "address": proxy_socket,
                "tls": ("plain_text", {}),
            })

        else:
            raise NotImplementedError("Unhandled proxy socket: %r" % proxy_socket)

        return

    if socket == 'disabled':
        site_cfg['disabled'] = True
        site_cfg['socket'] = ("local", None)
        return

    if isinstance(socket, str):
        site_cfg["socket"] = _migrate_string_encoded_socket(socket)


def _migrate_string_encoded_socket(value: str) -> Tuple[str, Union[Dict]]:
    family_txt, address = value.split(":", 1)

    if family_txt == "unix":
        return "unix", {
            "path": value.split(":", 1)[1],
        }

    if family_txt in ["tcp", "tcp6"]:
        host, port = address.rsplit(":", 1)
        return family_txt, {
            "address": (host, int(port)),
            "tls": ("plain_text", {}),
        }

    raise NotImplementedError()


#.
#   .--Sites---------------------------------------------------------------.
#   |                        ____  _ _                                     |
#   |                       / ___|(_) |_ ___  ___                          |
#   |                       \___ \| | __/ _ \/ __|                         |
#   |                        ___) | | ||  __/\__ \                         |
#   |                       |____/|_|\__\___||___/                         |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |  The config module provides some helper functions for sites.         |
#   '----------------------------------------------------------------------'


def default_single_site_configuration() -> SiteConfigurations:
    return {
        omd_site(): {
            'alias': _("Local site %s") % omd_site(),
            'socket': ("local", None),
            'disable_wato': True,
            'disabled': False,
            'insecure': False,
            'url_prefix': url_prefix(),
            'multisiteurl': '',
            'persist': False,
            'replicate_ec': False,
            'replication': None,
            'timeout': 5,
            'user_login': True,
            'proxy': None,
        }
    }


sites: SiteConfigurations = {}


def sitenames() -> List[SiteId]:
    return list(sites)


# TODO: Cleanup: Make clear that this function is used by the status GUI (and not WATO)
# and only returns the currently enabled sites. Or should we redeclare the "disabled" state
# to disable the sites at all?
# TODO: Rename this!
def allsites() -> SiteConfigurations:
    return {
        name: site(name)  #
        for name in sitenames()
        if not site(name).get("disabled", False)
    }


def configured_sites() -> SiteConfigurations:
    return {site_id: site(site_id) for site_id in sitenames()}


def has_wato_slave_sites() -> bool:
    return bool(wato_slave_sites())


def is_wato_slave_site() -> bool:
    return _has_distributed_wato_file() and not has_wato_slave_sites()


def _has_distributed_wato_file() -> bool:
    return os.path.exists(cmk.utils.paths.check_mk_config_dir + "/distributed_wato.mk") \
        and os.stat(cmk.utils.paths.check_mk_config_dir + "/distributed_wato.mk").st_size != 0


def get_login_sites() -> List[SiteId]:
    """Returns the WATO slave sites a user may login and the local site"""
    return get_login_slave_sites() + [omd_site()]


# TODO: All site listing functions should return the same data structure, e.g. a list of
#       pairs (site_id, site)
def get_login_slave_sites() -> List[SiteId]:
    """Returns a list of site ids which are WATO slave sites and users can login"""
    login_sites = []
    for site_id, site_spec in wato_slave_sites().items():
        if site_spec.get('user_login', True) and not site_is_local(site_id):
            login_sites.append(site_id)
    return login_sites


def wato_slave_sites() -> SiteConfigurations:
    return {
        site_id: s  #
        for site_id, s in sites.items()
        if s.get("replication")
    }


def sorted_sites() -> List[Tuple[SiteId, str]]:
    return sorted([(site_id, s['alias']) for site_id, s in user.authorized_sites().items()],
                  key=lambda k: k[1].lower())


def site(site_id: SiteId) -> SiteConfiguration:
    s = dict(sites.get(site_id, {}))
    # Now make sure that all important keys are available.
    # Add missing entries by supplying default values.
    s.setdefault("alias", site_id)
    s.setdefault("socket", ("local", None))
    s.setdefault("url_prefix", "../")  # relative URL from /check_mk/
    s["id"] = site_id
    return s


def site_is_local(site_id: SiteId) -> bool:
    family_spec, address_spec = site(site_id)["socket"]
    return _is_local_socket_spec(family_spec, address_spec)


def _is_local_socket_spec(family_spec: str, address_spec: Dict[str, Any]) -> bool:
    if family_spec == "local":
        return True

    if family_spec == "unix" and address_spec["path"] == cmk.utils.paths.livestatus_unix_socket:
        return True

    return False


def is_single_local_site() -> bool:
    if len(sites) > 1:
        return False
    if len(sites) == 0:
        return True

    # Also use Multisite mode if the one and only site is not local
    sitename = list(sites.keys())[0]
    return site_is_local(sitename)


def get_configured_site_choices() -> List[Tuple[SiteId, str]]:
    return site_choices(user.authorized_sites(unfiltered_sites=configured_sites()))


def site_attribute_default_value() -> Optional[SiteId]:
    site_id = omd_site()
    authorized_site_ids = user.authorized_sites(unfiltered_sites=configured_sites()).keys()
    if site_id in authorized_site_ids:
        return site_id
    return None


def site_choices(site_configs: SiteConfigurations) -> List[Tuple[SiteId, str]]:
    """Compute the choices to be used e.g. in dropdowns from a SiteConfigurations collection"""
    choices = []
    for site_id, site_spec in site_configs.items():
        title = site_id
        if site_spec.get("alias"):
            title += " - " + site_spec["alias"]

        choices.append((site_id, title))

    return sorted(choices, key=lambda s: s[1])


def get_event_console_site_choices() -> List[Tuple[SiteId, str]]:
    return site_choices({
        site_id: site
        for site_id, site in user.authorized_sites(unfiltered_sites=configured_sites()).items()
        if site_is_local(site_id) or site.get("replicate_ec", False)
    })


def get_activation_site_choices() -> List[Tuple[SiteId, str]]:
    return site_choices(activation_sites())


def activation_sites() -> SiteConfigurations:
    """Returns sites that are affected by WATO changes

    These sites are shown on activation page and get change entries
    added during WATO changes."""
    return {
        site_id: site
        for site_id, site in user.authorized_sites(unfiltered_sites=configured_sites()).items()
        if site_is_local(site_id) or site.get("replication")
    }
