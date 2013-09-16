<?php
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2013             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

if (substr($NAME[1], 0, 11) == 'Power_Meter') {
    $vlabel = "--vertical-label 'Watts'";
} elseif (substr($NAME[1], 0, 4) == 'Temp') {
    $vlabel = "--vertical-label 'Celsius'";
} else {
    $vlabel = "";
}

$opt[1] = "$vlabel -l0 -u60 --title \"IPMI sensor $NAME[1] / $hostname\" ";

$def[1] = "DEF:value=$RRDFILE[1]:$DS[1]:MAX ";
$def[1] .= "AREA:value#ffd040:\"Sensor $NAME[1] \\n\" ";
$def[1] .= "LINE:value#ff8000 ";

?>
