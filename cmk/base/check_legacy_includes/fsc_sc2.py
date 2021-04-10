#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# type: ignore[list-item,import,assignment,misc,operator]  # TODO: see which are needed in this file
from .fan import check_fan
from .temperature import check_temperature
#   .--CPU-----------------------------------------------------------------.
#   |                           ____ ____  _   _                           |
#   |                          / ___|  _ \| | | |                          |
#   |                         | |   | |_) | | | |                          |
#   |                         | |___|  __/| |_| |                          |
#   |                          \____|_|    \___/                           |
#   |                                                                      |
#   '----------------------------------------------------------------------'

# .1.3.6.1.4.1.231.2.10.2.2.10.6.4.1.3.1.1 "CPU1"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.4.1.3.1.2 "CPU2"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.4.1.4.1.1 3
# .1.3.6.1.4.1.231.2.10.2.2.10.6.4.1.4.1.2 2
# .1.3.6.1.4.1.231.2.10.2.2.10.6.4.1.5.1.1 "Intel(R) Xeon(R) CPU E5-2620 v2 @ 2.10GHz"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.4.1.5.1.2 ""
# .1.3.6.1.4.1.231.2.10.2.2.10.6.4.1.8.1.1 2100
# .1.3.6.1.4.1.231.2.10.2.2.10.6.4.1.8.1.2 0
# .1.3.6.1.4.1.231.2.10.2.2.10.6.4.1.13.1.1 6
# .1.3.6.1.4.1.231.2.10.2.2.10.6.4.1.13.1.2 0


def inventory_fsc_sc2_cpu_status(info):
    for line in info:
        if line[1] != '2':
            yield line[0], None


def check_fsc_sc2_cpu_status(item, _no_params, info):
    def get_cpu_status(status):
        return {
            '1': (3, 'unknown'),
            '2': (3, 'not-present'),
            '3': (0, 'ok'),
            '4': (0, 'disabled'),
            '5': (2, 'error'),
            '6': (2, 'failed'),
            '7': (1, 'missing-termination'),
            '8': (1, 'prefailure-warning'),
        }.get(status, (3, 'unknown'))

    for designation, status, model, speed, cores in info:
        if designation == item:
            status_state, status_txt = get_cpu_status(status)
            return status_state, 'Status is {0}, {1}, {2} cores @ {3} MHz'.format(
                status_txt, model, cores, speed)


#.
#   .--memory--------------------------------------------------------------.
#   |                                                                      |
#   |              _ __ ___   ___ _ __ ___   ___  _ __ _   _               |
#   |             | '_ ` _ \ / _ \ '_ ` _ \ / _ \| '__| | | |              |
#   |             | | | | | |  __/ | | | | | (_) | |  | |_| |              |
#   |             |_| |_| |_|\___|_| |_| |_|\___/|_|   \__, |              |
#   |                                                  |___/               |
#   '----------------------------------------------------------------------'

# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.3.1.1 "DIMM-1A"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.3.1.2 "DIMM-2A"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.3.1.3 "DIMM-3A"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.3.1.4 "DIMM-1B"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.3.1.5 "DIMM-2B"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.3.1.6 "DIMM-3B"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.3.1.7 "DIMM-1C"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.3.1.8 "DIMM-2C"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.3.1.9 "DIMM-3C"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.4.1.1 3
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.4.1.2 2
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.4.1.3 2
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.4.1.4 3
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.4.1.5 2
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.4.1.6 2
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.4.1.7 3
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.4.1.8 2
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.4.1.9 2
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.6.1.1 4096
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.6.1.2 -1
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.6.1.3 -1
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.6.1.4 4096
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.6.1.5 -1
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.6.1.6 -1
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.6.1.7 4096
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.6.1.8 -1
# .1.3.6.1.4.1.231.2.10.2.2.10.6.5.1.6.1.9 -1


def inventory_fsc_sc2_mem_status(info):
    for line in info:
        if line[1] != '2':
            yield line[0], None


def check_fsc_sc2_mem_status(item, _no_params, info):
    def get_mem_status(status):
        return {
            '1': (3, 'unknown'),
            '2': (3, 'not-present'),
            '3': (0, 'ok'),
            '4': (0, 'disabled'),
            '5': (2, 'error'),
            '6': (2, 'failed'),
            '7': (1, 'prefailure-predicted'),
            '11': (0, 'hidden'),
        }.get(status, (3, 'unknown'))

    for designation, status, capacity in info:
        if designation == item:
            status_state, status_txt = get_mem_status(status)
            return status_state, 'Status is {0}, Size {1} MB'.format(status_txt, capacity)


#.
#   .--fans----------------------------------------------------------------.
#   |                          __                                          |
#   |                         / _| __ _ _ __  ___                          |
#   |                        | |_ / _` | '_ \/ __|                         |
#   |                        |  _| (_| | | | \__ \                         |
#   |                        |_|  \__,_|_| |_|___/                         |
#   |                                                                      |
#   '----------------------------------------------------------------------'

# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.3.1.1 "FAN1 SYS"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.3.1.2 "FAN2 SYS"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.3.1.3 "FAN3 SYS"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.3.1.4 "FAN4 SYS"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.3.1.5 "FAN5 SYS"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.3.1.6 "FAN PSU1"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.3.1.7 "FAN PSU2"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.5.1.1 3
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.5.1.2 3
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.5.1.3 3
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.5.1.4 3
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.5.1.5 3
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.5.1.6 3
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.5.1.7 3
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.6.1.1 5820
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.6.1.2 6000
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.6.1.3 6000
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.6.1.4 6000
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.6.1.5 6120
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.6.1.6 2400
# .1.3.6.1.4.1.231.2.10.2.2.10.5.2.1.6.1.7 2400

FAN_FSC_SC2_CHECK_DEFAULT_PARAMETERS = {
    'lower': (1500, 2000),
}


def inventory_fsc_sc2_fans(info):
    for line in info:
        if line[1] not in ["8"]:
            yield line[0], {}


def check_fsc_sc2_fans(item, params, info):
    status_map = {
        '1': (3, 'Status is unknown'),
        '2': (0, 'Status is disabled'),
        '3': (0, 'Status is ok'),
        '4': (2, 'Status is failed'),
        '5': (1, 'Status is prefailure-predicted'),
        '6': (1, 'Status is redundant-fan-failed'),
        '7': (3, 'Status is not-manageable'),
        '8': (0, 'Status is not-present'),
    }

    if isinstance(params, tuple):
        params = {'lower': params}

    for designation, status, rpm in info:
        if designation == item:
            yield status_map.get(status, (3, 'Status is unknown'))
            if rpm:
                yield check_fan(int(rpm), params)
            else:
                yield 0, "Device did not deliver RPM values"


#.
#   .--power---------------------------------------------------------------.
#   |                                                                      |
#   |                    _ __   _____      _____ _ __                      |
#   |                   | '_ \ / _ \ \ /\ / / _ \ '__|                     |
#   |                   | |_) | (_) \ V  V /  __/ |                        |
#   |                   | .__/ \___/ \_/\_/ \___|_|                        |
#   |                   |_|                                                |
#   '----------------------------------------------------------------------'

# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.4.1.3.1 "CPU1 Power"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.4.1.3.2 "CPU2 Power"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.4.1.4.1 "HDD Power"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.4.1.7.1 "System Power"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.4.1.10.1 "PSU1 Power"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.4.1.10.2 "PSU2 Power"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.4.1.224.1 "Total Power"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.4.1.224.2 "Total Power Out"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.5.1.3.1 5
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.5.1.3.2 0
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.5.1.4.1 8
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.5.1.7.1 50
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.5.1.10.1 52
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.5.1.10.2 40
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.5.1.224.1 92
# .1.3.6.1.4.1.231.2.10.2.2.10.6.7.1.5.1.224.2 68


def parse_fsc_sc2_power_consumption(info):
    parsed = {}
    for designation, value in info:
        # sometimes the device does not return a value
        if not value:
            parsed.setdefault(designation,
                              {"device_state": (3, 'Error on device while reading value')})
        else:
            parsed.setdefault(designation, {"power": int(value)})
    return parsed


#.
#   .--info----------------------------------------------------------------.
#   |                          _        __                                 |
#   |                         (_)_ __  / _| ___                            |
#   |                         | | '_ \| |_ / _ \                           |
#   |                         | | | | |  _| (_) |                          |
#   |                         |_|_| |_|_|  \___/                           |
#   |                                                                      |
#   '----------------------------------------------------------------------'

# .1.3.6.1.4.1.231.2.10.2.2.10.2.3.1.5.1 "PRIMERGY RX300 S8"
# .1.3.6.1.4.1.231.2.10.2.2.10.2.3.1.7.1 "--"
# .1.3.6.1.4.1.231.2.10.2.2.10.4.1.1.11.1 "V4.6.5.4 R1.6.0 for D2939-B1x"


def inventory_fsc_sc2_info(info):
    if info:
        return [(None, None)]


def check_fsc_sc2_info(_no_item, _no_params, info):
    if info:
        return (0, 'Model: {0}, Serial Number: {1}, BIOS Version: {2}'.format(
            info[0][0], info[0][1], info[0][2]))


#.
#   .--temperature---------------------------------------------------------.
#   |      _                                      _                        |
#   |     | |_ ___ _ __ ___  _ __   ___ _ __ __ _| |_ _   _ _ __ ___       |
#   |     | __/ _ \ '_ ` _ \| '_ \ / _ \ '__/ _` | __| | | | '__/ _ \      |
#   |     | ||  __/ | | | | | |_) |  __/ | | (_| | |_| |_| | | |  __/      |
#   |      \__\___|_| |_| |_| .__/ \___|_|  \__,_|\__|\__,_|_|  \___|      |
#   |                       |_|                                            |
#   '----------------------------------------------------------------------'

# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.3.1.1 "Ambient"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.3.1.2 "Systemboard 1"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.3.1.3 "Systemboard 2"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.3.1.4 "CPU1"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.3.1.5 "CPU2"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.3.1.6 "MEM A"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.3.1.7 "MEM B"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.3.1.8 "MEM C"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.3.1.9 "MEM D"
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.5.1.1 8
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.5.1.2 8
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.5.1.3 8
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.5.1.4 8
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.5.1.5 2
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.5.1.6 8
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.5.1.7 8
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.5.1.8 8
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.5.1.9 8
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.6.1.1 26
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.6.1.2 27
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.6.1.3 33
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.6.1.4 27
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.6.1.5 0
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.6.1.6 28
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.6.1.7 28
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.6.1.8 27
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.6.1.9 27
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.7.1.1 37
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.7.1.2 75
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.7.1.3 75
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.7.1.4 77
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.7.1.5 89
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.7.1.6 78
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.7.1.7 78
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.7.1.8 78
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.7.1.9 78
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.8.1.1 42
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.8.1.2 80
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.8.1.3 80
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.8.1.4 81
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.8.1.5 93
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.8.1.6 82
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.8.1.7 82
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.8.1.8 82
# .1.3.6.1.4.1.231.2.10.2.2.10.5.1.1.8.1.9 82


def inventory_fsc_sc2_temp(info):
    for line in info:
        if line[1] != '2':
            yield line[0], {}


def check_fsc_sc2_temp(item, params, info):
    temp_status = {
        '1': (3, 'unknown'),
        '2': (0, 'not-available'),
        '3': (0, 'ok'),
        '4': (2, 'sensor-failed'),
        '5': (2, 'failed'),
        '6': (1, 'temperature-warning-toohot'),
        '7': (2, 'temperature-critical-toohot'),
        '8': (0, 'temperature-normal'),
        '9': (1, 'temperature-warning')
    }

    for designation, status, temp, dev_warn, dev_crit in info:
        if designation == item:
            if not temp:
                return 3, 'Did not receive temperature data'

            dev_status, dev_status_name = temp_status.get(status, (3, 'unknown'))

            if not dev_warn or not dev_crit:
                return 3, 'Did not receive device levels'

            dev_levels = int(dev_warn), int(dev_crit)

            return check_temperature(int(temp), params, 'temp_{}'.format(item.replace(' ', '_')),
                                     'c', dev_levels, None, dev_status, dev_status_name)


#.
#   .--voltage-------------------------------------------------------------.
#   |                             _ _                                      |
#   |                 __   _____ | | |_ __ _  __ _  ___                    |
#   |                 \ \ / / _ \| | __/ _` |/ _` |/ _ \                   |
#   |                  \ V / (_) | | || (_| | (_| |  __/                   |
#   |                   \_/ \___/|_|\__\__,_|\__, |\___|                   |
#   |                                        |___/                         |
#   '----------------------------------------------------------------------'

# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.3.1.1 "BATT 3.0V"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.3.1.2 "STBY 12V"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.3.1.3 "STBY 5V"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.3.1.4 "STBY 3.3V"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.3.1.5 "LAN 1.8V STBY"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.3.1.6 "iRMC 1.5V STBY"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.3.1.7 "LAN 1.0V STBY"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.3.1.8 "MAIN 12V"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.3.1.9 "MAIN 5V"
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.4.1.1 3
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.4.1.2 3
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.4.1.3 3
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.4.1.4 3
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.4.1.5 3
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.4.1.6 3
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.4.1.7 3
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.4.1.8 3
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.4.1.9 3
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.5.1.1 3270
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.5.1.2 11880
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.5.1.3 5100
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.5.1.4 3350
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.5.1.5 1800
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.5.1.6 1460
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.5.1.7 980
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.5.1.8 12160
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.5.1.9 4980
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.7.1.1 2010
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.7.1.2 11280
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.7.1.3 4630
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.7.1.4 3020
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.7.1.5 1670
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.7.1.6 1390
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.7.1.7 930
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.7.1.8 11310
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.7.1.9 4630
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.8.1.1 3500
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.8.1.2 12960
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.8.1.3 5420
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.8.1.4 3570
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.8.1.5 1930
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.8.1.6 1610
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.8.1.7 1080
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.8.1.8 12900
# .1.3.6.1.4.1.231.2.10.2.2.10.6.3.1.8.1.9 5420


def parse_fsc_sc2_voltage(info):
    # dev_state:
    # sc2VoltageStatus OBJECT-TYPE
    # SYNTAX       INTEGER
    # {
    #     unknown(1),
    #     not-available(2),
    #     ok(3),
    #     too-low(4),
    #     too-high(5),
    #     sensor-failed(6)
    # }
    # ACCESS       read-only
    # STATUS       mandatory
    # DESCRIPTION  "Voltage status"
    # ::= { sc2Voltages 4 }

    parsed = {}
    for designation, dev_state, value, min_value, max_value in info:
        if dev_state == "2":
            continue
        try:
            value = float(value) / 1000.0
            min_value = float(min_value) / 1000.0
            max_value = float(max_value) / 1000.0
        except ValueError:
            state_info = 3, 'Could not get all values'
            parsed.setdefault(designation, {"device_state": state_info})
        else:
            state_info = value
            if value < min_value:
                state_info = value, (2, 'too low, deceeds %.2f V' % min_value)
            elif value >= max_value:
                state_info = value, (2, 'too high, exceeds %.2f V' % max_value)
            parsed.setdefault(designation, {"voltage": state_info})
    return parsed
