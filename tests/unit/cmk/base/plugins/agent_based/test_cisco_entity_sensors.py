#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from cmk.base.plugins.agent_based.cisco_entity_sensors import (
    parse_cisco_entity_sensors,
)

from cmk.base.plugins.agent_based.utils.entity_sensors import (
    EntitySensor,
)
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    State,
    Service,
    Result,
)

from cmk.base.plugins.agent_based.entity_sensors import (
    check_entity_sensors_fan,
    check_entity_sensors_power_presence,
    discover_entity_sensors_fan,
    discover_entity_sensors_power_presence,
)

_string_table = [
    [['9', 'CHASSIS-1'], ['10', ''], ['11', 'FAN-1'], ['12', ''], ['13', ''], ['14', ''], ['15', 'PSU-1'], ['16', ''],
     ['17', 'MEMORY-1'], ['18', ''], ['19', ''], ['20', ''], ['21', 'SSD-1'], ['22', ''], ['23', 'CPU-1'], ['24', ''],
     ['25', '']],
    [['26', '8', '9', '31', '1', '397951198'], ['27', '0', '9', '0', '1', '397951198'],
     ['28', '0', '9', '0', '1', '397951198'], ['29', '0', '9', '0', '1', '397951198'],
     ['30', '8', '9', '48', '1', '397951198'], ['31', '8', '9', '48', '1', '397951198'],
     ['32', '8', '9', '48', '1', '397951198'], ['33', '8', '9', '48', '1', '397951198'],
     ['34', '8', '9', '48', '1', '397951198'], ['35', '8', '9', '48', '1', '397951198'],
     ['36', '8', '9', '49', '1', '397951198'], ['37', '8', '9', '49', '1', '397951198'],
     ['38', '8', '9', '50', '1', '397951198'], ['39', '8', '9', '50', '1', '397951198'],
     ['40', '8', '9', '48', '1', '397951198'], ['41', '8', '9', '48', '1', '397951198'],
     ['42', '8', '9', '47', '1', '397951198'], ['43', '8', '9', '47', '1', '397951199'],
     ['44', '8', '9', '48', '1', '397951199'], ['45', '8', '9', '48', '1', '397951199'],
     ['46', '0', '9', '0', '1', '397951199'], ['47', '10', '9', '2820', '1', '397951199'],
     ['48', '12', '9', '1', '1', '397951199'], ['49', '0', '9', '0', '1', '397951199'],
     ['50', '0', '9', '0', '1', '397951199'], ['51', '0', '9', '0', '1', '397951199'],
     ['52', '0', '9', '0', '1', '397951199'], ['53', '0', '9', '0', '1', '397951199'],
     ['54', '0', '9', '0', '1', '397951199'], ['55', '0', '9', '0', '1', '397951199'],
     ['56', '0', '9', '0', '1', '397951199'], ['57', '0', '9', '0', '1', '397951199'],
     ['58', '0', '9', '0', '1', '397951199'], ['59', '0', '9', '0', '1', '397951199'],
     ['60', '0', '9', '0', '1', '397951199'], ['61', '0', '9', '0', '1', '397951199'],
     ['62', '0', '9', '0', '1', '397951199'], ['63', '0', '9', '0', '1', '397951199'],
     ['64', '0', '9', '0', '1', '397951199'], ['65', '0', '9', '0', '1', '397951199'],
     ['66', '0', '9', '0', '1', '397951199'], ['67', '0', '9', '0', '1', '397951199'],
     ['68', '0', '9', '0', '1', '397951200'], ['69', '0', '9', '0', '1', '397951200'],
     ['70', '0', '9', '0', '1', '397951200'], ['71', '0', '9', '0', '1', '397951200'],
     ['72', '0', '9', '0', '1', '397951200'], ['73', '0', '9', '0', '1', '397951200'],
     ['74', '0', '9', '0', '1', '397951200'], ['75', '0', '9', '0', '1', '397951200']]]

_section = {
    'fan': {
        'Sensor 47': EntitySensor(name='Sensor 47', reading=2820.0, unit='RPM', state=State.OK, status_descr='OK'),
    },
    'power_presence': {
        'Sensor 48': EntitySensor(name='Sensor 48', reading=1.0, unit='boolean', state=State.OK, status_descr='OK'),
    },
}


@pytest.mark.parametrize('string_table, expected_section', [
    pytest.param(
        _string_table,
        _section,
        id='Parse: Cisco entity Sensors'
    ),
])
def test_parse_cisco_entity_sensors(string_table, expected_section):
    assert parse_cisco_entity_sensors(string_table) == expected_section


@pytest.mark.parametrize('string_table, expected_discovery', [
    pytest.param(
        _string_table,
        [
            Service(item='Sensor 47'),
        ],
        id='Discover: Cisco entity FAN Sensors'
    ),
])
def test_discover_entity_sensors_fan(string_table, expected_discovery):
    assert list(discover_entity_sensors_fan(
        parse_cisco_entity_sensors(string_table))) == expected_discovery


@pytest.mark.parametrize('string_table, expected_discovery', [
    pytest.param(
        _string_table,
        [
            Service(item='Sensor 48'),
        ],
        id='Discover: Cisco entity Power presence Sensors'
    ),
])
def test_discover_entity_sensors_power_presence(string_table, expected_discovery):
    assert list(discover_entity_sensors_power_presence(
        parse_cisco_entity_sensors(string_table))) == expected_discovery


@pytest.mark.parametrize('item, params, section, expected_result', [
    pytest.param(
        'Sensor 47',
        {
            'lower': (2000, 1000),
        },
        _section,
        [
            Result(state=State.OK, summary='Operational status: OK'),
            Result(state=State.OK, summary='Speed: 2820 RPM'),
        ],
        id='Check: Cisco entity Fan Sensors'
    ),
])
def test_check_entity_sensors_fan(item, params, section, expected_result):
    assert list(check_entity_sensors_fan(item, params, section)) == expected_result


@pytest.mark.parametrize('item, params, section, expected_result', [
    pytest.param(
        'Sensor 48',
        {
            'power_off_criticality': 1,
        },
        _section,
        [
            Result(state=State.OK, summary='Powered on'),
        ],
        id='Check: Cisco entity power presence Sensors'
    ),
])
def test_check_entity_sensors_power_presence(item, params, section, expected_result):
    assert list(check_entity_sensors_power_presence(item, params, section)) == expected_result
