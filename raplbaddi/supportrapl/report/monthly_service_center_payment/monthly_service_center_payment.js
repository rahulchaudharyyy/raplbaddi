// Copyright (c) 2024, Nishant Bhickta and contributors
// For license information, please see license.txt

frappe.query_reports["Monthly Service Center Payment"] = {
	"filters": [
		{
			'fieldname':'service_centre',
			'label':__('Service Centre'),
			'fieldtype':'Link',
			'options':'Service Centre'
		},
		{
			'fieldname':'months',
			'label':__('Months'),
			'fieldtype':'Link',
			'options':'Months'
		}
	]
};
