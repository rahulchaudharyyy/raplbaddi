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
			"fieldname": "brand_name",
			"label": "Brand Name",
			"fieldtype": "Link",
			"options": "Brand"
		},
		{
			"fieldname": "geyser_model",
			"label": "Geyser Model",
			"fieldtype": "Link",
			"options": "Geyser Model"
		},
		{
			"fieldname": "capacity",
			"label": "Geyser Capacity",
			"fieldtype": "Link",
			"options": "Geyser Capacity"
		},
		// {
		// 	"fieldname":"month",
		// 	"label": __("Month"),
		// 	"fieldtype": "Select",
		// 	"options": " \nJan\nFeb\nMar\nApr\nMay\nJun\nJul\nAug\nSep\nOct\nNov\nDec",
		// },
	],
};
