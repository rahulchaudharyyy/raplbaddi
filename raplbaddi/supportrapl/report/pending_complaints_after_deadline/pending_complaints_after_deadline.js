// Copyright (c) 2024, Nishant Bhickta and contributors
// For license information, please see license.txt

frappe.query_reports["Pending Complaints After Deadline"] = {
	"filters": [
		{
			'fieldname': 'group_by_date',
			'label': __('Group By Date'),
			'fieldtype': 'Check',
			'default': 1,
			'hidden':1
		}
	]
};
