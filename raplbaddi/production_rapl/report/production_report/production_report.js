// Copyright (c) 2023, Nishant Bhickta and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Production Report"] = {
	"filters": [
		{
			"fieldname": "item",
			"label": "Item",
			"fieldtype": "Select",
			"options": "Geyser\nDesert Air Cooler\nElement",
			"default": "Geyser"
		},
		{
			"fieldname": "start_date",
			"label": "Starting Date of Production",
			"fieldtype": "Date",
			"default": frappe.datetime.year_start()
		},
		{
			"fieldname": "end_date",
			"label": "Ending Date of Production",
			"fieldtype": "Date",
			"default": frappe.datetime.year_end()
		},
		{
			"fieldname": "group_by_item_model_capacity_brand",
			"label": "Group By Item Model Capcity Brand",
			"fieldtype": "Check"
		},
	],
};



		// {
		// 	"fieldname":"month",
		// 	"label": __("Month"),
		// 	"fieldtype": "Select",
		// 	"options": " \nJan\nFeb\nMar\nApr\nMay\nJun\nJul\nAug\nSep\nOct\nNov\nDec",
		// },
