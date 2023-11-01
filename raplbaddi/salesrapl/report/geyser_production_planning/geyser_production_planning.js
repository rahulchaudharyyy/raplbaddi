// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Geyser Production Planning"] = {
	"filters": [
		{
			"fieldname": "report_type",
			"label": __("Report Type"),
			"fieldtype": "Select",
			"options": "Order and Shortage\nItemwise Order and Shortage",
			"reqd": 1,
			"default": "Order and Shortage"
		},
	]
};
