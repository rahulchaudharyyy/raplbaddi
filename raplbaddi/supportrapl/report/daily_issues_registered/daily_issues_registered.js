// Copyright (c) 2024, Nishant Bhickta and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Issues Registered"] = {
<<<<<<< Updated upstream
	onload : function(report){
		report.page.add_inner_button(__("Today"), function () {
		frappe.query_report.get_filter('start_date').set_value(frappe.datetime.get_today());
	});

	},

	"filters": [
		{
			'fieldname': 'start_date',
			'label': __('Start Date'),
			'fieldtype': 'Date',
			'reqd': 1,
			'hidden': 1
		}
=======
	"filters": [

>>>>>>> Stashed changes
	]
};
