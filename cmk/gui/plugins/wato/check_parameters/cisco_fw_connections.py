#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    Tuple,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)


def _parameter_valuespec_cisco_fw_connections():
    return Dictionary(elements=[
        ("connections",
         Tuple(
             help=_("This rule sets upper limits to the current number of connections through "
                    "a Cisco PIX/ASA/FirePower firewall."),
             title=_("Maximum number of firewall connections"),
             elements=[
                 Integer(title=_("Warning at")),
                 Integer(title=_("Critical at")),
             ],
         )),
        ("connections_lower",
         Tuple(
             help=_("This rule sets lower limits to the current number of connections through "
                    "a Cisco PIX/ASA/FirePower firewall."),
             title=_("Minimum number of firewall connections"),
             elements=[
                 Integer(title=_("Warning at")),
                 Integer(title=_("Critical at")),
             ],
         )),
    ],)


rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="cisco_fw_connections",
        group=RulespecGroupCheckParametersApplications,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_cisco_fw_connections,
        title=lambda: _("Cisco Firewall Connections"),
    ))
