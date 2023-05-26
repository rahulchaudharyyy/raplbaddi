// Copyright (c) 2023, Nishant Bhickta and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Detailed Report Geyser Testing"] = {
	"filters": [
		{
			fieldname: 'serial_no',
			label: 'Serial Number',
			fieldtype: 'Link',
			options: 'Daily Production Item'
		},
		{
			fieldname: 'start_date',
			label: 'Start Date',
			fieldtype: 'Date',
			default: dateutil.year_start()
		},
		{
			fieldname: 'end_date',
			label: 'End Date',
			fieldtype: 'Date',
			default: dateutil.year_end()
		}
	]
};
