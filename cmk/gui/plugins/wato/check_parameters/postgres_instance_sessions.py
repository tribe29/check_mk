#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    TextAscii,
    Tuple,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)


def _parameter_valuespec_postgres_instance_sessions():
    return Dictionary(
        help=_("This check monitors the current number of active and idle sessions on PostgreSQL"),
        elements=[
            (
                "total",
                Tuple(
                    title=_("Number of current sessions"),
                    elements=[
                        Integer(title=_("Warning at"), unit=_("sessions"), default_value=100),
                        Integer(title=_("Critical at"), unit=_("sessions"), default_value=200),
                    ],
                ),
            ),
            (
                "running",
                Tuple(
                    title=_("Number of currently running sessions"),
                    help=_("Levels for the number of sessions that are currently active"),
                    elements=[
                        Integer(title=_("Warning at"), unit=_("sessions"), default_value=10),
                        Integer(title=_("Critical at"), unit=_("sessions"), default_value=20),
                    ],
                ),
            ),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="postgres_instance_sessions",
        group=RulespecGroupCheckParametersApplications,
        item_spec=lambda: TextAscii(title=_("Instance")),
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_postgres_instance_sessions,
        title=lambda: _("PostgreSQL Sessions"),
    ))
