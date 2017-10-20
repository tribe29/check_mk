// +------------------------------------------------------------------+
// |             ____ _               _        __  __ _  __           |
// |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
// |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
// |           | |___| | | |  __/ (__|   <    | |  | | . \            |
// |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
// |                                                                  |
// | Copyright Mathias Kettner 2014             mk@mathias-kettner.de |
// +------------------------------------------------------------------+
//
// This file is part of Check_MK.
// The official homepage is at http://mathias-kettner.de/check_mk.
//
// check_mk is free software;  you can redistribute it and/or modify it
// under the  terms of the  GNU General Public License  as published by
// the Free Software Foundation in version 2.  check_mk is  distributed
// in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
// out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
// PARTICULAR PURPOSE. See the  GNU General Public License for more de-
// tails. You should have  received  a copy of the  GNU  General Public
// License along with GNU Make; see the file  COPYING.  If  not,  write
// to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
// Boston, MA 02110-1301 USA.

#include "ServiceContactsColumn.h"
#include <unordered_set>
#include "Renderer.h"
#include "Row.h"
#include "nagios.h"

void ServiceContactsColumn::output(Row row, RowRenderer &r,
                                   const contact *auth_user) const {
    ListRenderer l(r);
    for (const auto &name : getValue(row, auth_user)) {
        l.output(name);
    }
}

std::vector<std::string> ServiceContactsColumn::getValue(
    Row row, const contact * /*auth_user*/) const {
    std::unordered_set<std::string> names;
    if (auto svc = columnData<service>(row)) {
        for (auto cm = svc->contacts; cm != nullptr; cm = cm->next) {
            names.insert(cm->contact_ptr->name);
        }
        for (auto cgm = svc->contact_groups; cgm != nullptr; cgm = cgm->next) {
            for (auto cm = cgm->group_ptr->members; cm != nullptr;
                 cm = cm->next) {
                names.insert(cm->contact_ptr->name);
            }
        }
    }
    return std::vector<std::string>(names.begin(), names.end());
}
