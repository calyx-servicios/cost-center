# -*- coding: utf-8 -*-
# Copyright <2019> <Calyx Servicios>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Cost and Revenue Center ",
    "summary": "Module summary",
    "version": "11.0.1.0.0",
    "development_status": "Alpha",
    "category": "Uncategorized",
    "website": " ",
    "author": "Calyx Servicios",
    "maintainers": ["mariodmoreno"],
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
        "account",
    ],
    "data": [
        # "security/ir.model.access.csv",
        "security/cost_center_security.xml",
        "views/cost_center_view.xml",
        "menuitems.xml"
    ],
}
