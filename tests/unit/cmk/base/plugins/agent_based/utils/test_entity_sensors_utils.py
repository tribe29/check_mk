#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest
from cmk.base.plugins.agent_based.utils.entity_sensors import (
    parse_entity_sensors,
)
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    State,
)
from cmk.base.plugins.agent_based.utils.entity_sensors import (
    EntitySensor,
)

_string_table_fp1140 = [
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

_section_fp1140 = {
    'fan': {
        'Sensor 47': EntitySensor(name='Sensor 47', reading=2820.0, unit='RPM', state=State.OK, status_descr='OK'),
    },
    'power_presence': {
        'Sensor 48': EntitySensor(name='Sensor 48', reading=1.0, unit='boolean', state=State.OK, status_descr='OK'),
    },
}


@pytest.mark.parametrize("string_table, sensor_types_ignore, expected_section", [
    pytest.param(
        [
            [
                ['1', 'PA-500'],
                ['2', 'Fan #1 Operational'],
                ['3', 'Fan #2 Operational'],
                ['4', 'Temperature at MP [U6]'],
                ['5', 'Temperature at DP [U7]'],
            ],
            [
                ['2', '10', '9', '1', '1', 'rpm'],
                ['3', '10', '9', '1', '1', 'rpm'],
                ['4', '8', '9', '37', '1', 'celsius'],
                ['5', '8', '9', '40', '1', 'fahrenheit'],
            ],
        ],
        None,
        {
            'fan': {
                'Sensor 1 Operational': EntitySensor(
                    name='Sensor 1 Operational',
                    unit='RPM',
                    reading=1.0,
                    status_descr='OK',
                    state=State.OK,
                ),
                'Sensor 2 Operational': EntitySensor(
                    name='Sensor 2 Operational',
                    unit='RPM',
                    reading=1.0,
                    status_descr='OK',
                    state=State.OK,
                ),
            },
            'temp': {
                'Sensor at MP [U6]': EntitySensor(
                    name='Sensor at MP [U6]',
                    unit='c',
                    reading=37.0,
                    status_descr='OK',
                    state=State.OK,
                ),
                'Sensor at DP [U7]': EntitySensor(
                    name='Sensor at DP [U7]',
                    unit='f',
                    reading=40.0,
                    status_descr='OK',
                    state=State.OK,
                ),
            },
        },
        id='Parse: Entity Sensors PA-500'
    ),
    pytest.param(
        [
            [
                ['1', 'Chassis'],
                ['2', 'Processor 0/0'],
                ['3', 'Processor 0/1'],
                ['4', 'Processor 0/2'],
                ['5', 'Processor 0/3'],
                ['6', 'Processor 0/4'],
                ['7', 'Processor 0/5'],
                ['8', 'Processor 0/6'],
                ['9', 'Processor 0/7'],
                ['10', 'AS Slot for Removable Drive 0'],
                ['11', 'AS5 Slot for Removable Drive 1'],
                ['12', 'Mi_M6 Removable Drive in Slot 0'],
                ['13', 'Mi_M6_M Removable Drive in Slot 1'],
                ['14', 'Chassis Cooling Fan 1'],
                ['15', 'Chassis Fan Sensor 1'],
                ['16', 'Chassis Cooling Fan 2'],
                ['17', 'Chassis Fan Sensor 2'],
                ['18', 'Chassis Cooling Fan 3'],
                ['19', 'Chassis Fan Sensor 3'],
                ['20', 'Power Supply 0'],
                ['21', 'Power Supply 0 Presence Sensor'],
                ['22', 'Power Supply 0 Input Sensor'],
                ['23', 'Power Supply 0 Fan'],
                ['24', 'Power Supply 0 Fan Sensor'],
                ['25', 'Power Supply 0 Temperature Sensor'],
                ['26', 'Power Supply 1'],
                ['27', 'Power Supply 1 Presence Sensor'],
                ['28', 'Power Supply 1 Input Sensor'],
                ['29', 'Power Supply 1 Fan'],
                ['30', 'Power Supply 1 Fan Sensor'],
                ['31', 'Power Supply 1 Temperature Sensor'],
                ['32', 'CPU Temperature Sensor 0/0'],
                ['33', 'Chassis Ambient Temperature Sensor 1'],
                ['34', 'Chassis Ambient Temperature Sensor 2'],
                ['35', 'Chassis Ambient Temperature Sensor 3'],
                ['36', 'G0'],
                ['37', 'G1'],
                ['38', 'G2'],
                ['39', 'G3'],
                ['40', 'G4'],
                ['41', 'G5'],
                ['42', 'G6'],
                ['43', 'G7'],
                ['44', 'I0'],
                ['45', 'I1'],
                ['46', 'M0'],
            ],
            [
                ['15', '10', '9', '4864', '1', 'rpm'],
                ['17', '10', '9', '4864', '1', 'rpm'],
                ['19', '10', '9', '4864', '1', 'rpm'],
                ['21', '12', '9', '1', '1', 'truthvalue'],
                ['22', '12', '9', '1', '1', 'truthvalue'],
                ['24', '10', '9', '8448', '1', 'rpm'],
                ['25', '8', '9', '25', '1', 'celsius'],
                ['27', '12', '9', '1', '1', 'truthvalue'],
                ['28', '12', '9', '1', '1', 'truthvalue'],
                ['30', '10', '9', '8448', '1', 'rpm'],
                ['31', '8', '9', '23', '1', 'celsius'],
                ['32', '8', '9', '66', '1', 'celsius'],
                ['33', '8', '9', '37', '1', 'celsius'],
                ['34', '8', '9', '28', '1', 'celsius'],
                ['35', '8', '9', '39', '1', 'celsius'],
            ],
        ],
        None,
        {
            'fan': {
                'Sensor Chassis 1': EntitySensor(
                    name='Sensor Chassis 1',
                    reading=4864.0,
                    unit='RPM',
                    state=State.OK,
                    status_descr='OK',
                ),
                'Sensor Chassis 2': EntitySensor(
                    name='Sensor Chassis 2',
                    reading=4864.0,
                    unit='RPM',
                    state=State.OK,
                    status_descr='OK',
                ),
                'Sensor Chassis 3': EntitySensor(
                    name='Sensor Chassis 3',
                    reading=4864.0,
                    unit='RPM',
                    state=State.OK,
                    status_descr='OK',
                ),
                'Sensor Power Supply 0': EntitySensor(
                    name='Sensor Power Supply 0',
                    reading=8448.0,
                    unit='RPM',
                    state=State.OK,
                    status_descr='OK',
                ),
                'Sensor Power Supply 1': EntitySensor(
                    name='Sensor Power Supply 1',
                    reading=8448.0,
                    unit='RPM',
                    state=State.OK,
                    status_descr='OK',
                )
            },
            'power_presence': {
                'Sensor Power Supply 0 Presence': EntitySensor(
                    name='Sensor Power Supply 0 Presence',
                    reading=1.0,
                    unit='boolean',
                    state=State.OK,
                    status_descr='OK',
                ),
                'Sensor Power Supply 0 Input': EntitySensor(
                    name='Sensor Power Supply 0 Input',
                    reading=1.0,
                    unit='boolean',
                    state=State.OK,
                    status_descr='OK',
                ),
                'Sensor Power Supply 1 Presence': EntitySensor(
                    name='Sensor Power Supply 1 Presence',
                    reading=1.0,
                    unit='boolean',
                    state=State.OK,
                    status_descr='OK',
                ),
                'Sensor Power Supply 1 Input': EntitySensor(
                    name='Sensor Power Supply 1 Input',
                    reading=1.0,
                    unit='boolean',
                    state=State.OK,
                    status_descr='OK',
                )
            },
            'temp': {
                'Sensor Power Supply 0': EntitySensor(
                    name='Sensor Power Supply 0',
                    reading=25.0,
                    unit='c',
                    state=State.OK,
                    status_descr='OK',
                ),
                'Sensor Power Supply 1': EntitySensor(
                    name='Sensor Power Supply 1',
                    reading=23.0,
                    unit='c',
                    state=State.OK,
                    status_descr='OK',
                ),
                'Sensor CPU 0/0': EntitySensor(
                    name='Sensor CPU 0/0',
                    reading=66.0,
                    unit='c',
                    state=State.OK,
                    status_descr='OK',
                ),
                'Sensor Chassis Ambient 1': EntitySensor(
                    name='Sensor Chassis Ambient 1',
                    reading=37.0,
                    unit='c',
                    state=State.OK,
                    status_descr='OK',
                ),
                'Sensor Chassis Ambient 2': EntitySensor(
                    name='Sensor Chassis Ambient 2',
                    reading=28.0,
                    unit='c',
                    state=State.OK,
                    status_descr='OK',
                ),
                'Sensor Chassis Ambient 3': EntitySensor(
                    name='Sensor Chassis Ambient 3',
                    reading=39.0,
                    unit='c',
                    state=State.OK,
                    status_descr='OK',
                ),
            },
        },
        id='Parse: Entity Sensors with sensor name'
    ),
    pytest.param(
        _string_table_fp1140,
        {'0', '8'},
        _section_fp1140,
        id='Parse: Cisco entity Sensors Firepower 1140'
    ),
])
def test_parse_entity_sensors(string_table, sensor_types_ignore, expected_section):
    assert parse_entity_sensors(string_table, sensor_types_ignore) == expected_section
