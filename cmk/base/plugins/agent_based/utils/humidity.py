#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from ..agent_based_api.v1 import (
    check_levels,
    render,
)

def check_humidity(humidity, params):
    if isinstance(params, dict):
        levels = ((params.get("levels") or (None, None)) + (params.get("levels_lower") or
                                                            (None, None)))
    elif isinstance(params, (list, tuple)):
        # old params = (crit_low , warn_low, warn, crit)
        levels = (params[2], params[3], params[1], params[0])
    else:
        levels = (None, None, None, None)

    yield from check_levels(
        humidity,
        metric_name="humidity",
        levels_upper=(levels[0], levels[1]),
        levels_lower=(levels[2], levels[3]),
        render_func=render.percent,
        boundaries=(0, 100),
    )
