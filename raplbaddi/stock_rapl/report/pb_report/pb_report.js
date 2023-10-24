// Copyright (c) 2023, Nishant Bhickta and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PB Report"] = {
	"filters": [
		{
			"fieldname": "report_type",
			"label": __("Report Type"),
			"fieldtype": "Select",
			"options": "Box Dispatch\nBox Production"
		},
		{
			"fieldname": "add_priority",
			"label": __("Add Priority"),
			"fieldtype": "Check"
		},
		{
			"fieldname": "over_stock",
			"label": __("Add Over Stock"),
			"fieldtype": "Check"
		},
		{
			"fieldname": "add_links",
			"label": __("Add Links"),
			"fieldtype": "Check"
		}
	]
};
