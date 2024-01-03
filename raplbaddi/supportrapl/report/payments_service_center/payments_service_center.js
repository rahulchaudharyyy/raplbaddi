// Copyright (c) 2024, Nishant Bhickta and contributors
// For license information, please see license.txt

frappe.query_reports["Payments Service Center"] = {
	"filters": [
		{
			'fieldname':'Service_Centre',
			'label': __('Service Centre'),
			'fieldtype':'Link',
			'options':'Service Centre'
		},
		{
			'fieldname': 'start_date',
			'label': __('Start Date'),
			'fieldtype': 'Date'
		},
		{
			'fieldname': 'end_date',
			'label': __('End Date'),
			'fieldtype': 'Date'
		}	

	]
};
