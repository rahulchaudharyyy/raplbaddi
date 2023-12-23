// Copyright (c) 2023, Nishant Bhickta and contributors
// For license information, please see license.txt

frappe.query_reports["DSR Expense Analysis"] = {
	"filters": [
			{
				'fieldname':'sales_person',
				'label':__('Sales Person'),
				'fieldtype':'Link',
				'options':'Sales Person'

			}
	]
};
