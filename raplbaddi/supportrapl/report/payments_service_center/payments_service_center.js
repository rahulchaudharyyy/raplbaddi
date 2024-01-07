// Copyright (c) 2024, Nishant Bhickta and contributors
// For license information, please see license.txt

frappe.query_reports["Payments Service Center"] = {
	onload: function(report) {
		// arr = frappe.datetime.get_today().split("-")
        // arr.push("0" + (parseInt(arr.pop()) - 1))
        // yesterday = arr.join("-") 

        report.page.add_inner_button(__("Today"), function() {
            frappe.query_report.get_filter('start_date').set_value(frappe.datetime.get_today());
            frappe.query_report.get_filter('end_date').set_value(frappe.datetime.get_today());
        }, "Range");
        // report.page.add_inner_button(__("Yesterday"), function() {
        //     frappe.query_report.get_filter('start_date').set_value(yesterday);
        //     frappe.query_report.get_filter('end_date').set_value(yesterday);
        // }, "Range");
        report.page.add_inner_button(__("Week"), function() {
            frappe.query_report.get_filter('start_date').set_value(frappe.datetime.week_start());
            frappe.query_report.get_filter('end_date').set_value(frappe.datetime.week_end());
        }, "Range");
		report.page.add_inner_button(__("Month"), function() {
			frappe.query_report.get_filter('start_date').set_value(frappe.datetime.month_start());
			frappe.query_report.get_filter('end_date').set_value(frappe.datetime.month_end());
		}, "Range");
		report.page.add_inner_button(__("Quarter"), function() {
			frappe.query_report.get_filter('start_date').set_value(frappe.datetime.quarter_start());
			frappe.query_report.get_filter('end_date').set_value(frappe.datetime.quarter_end());
		}, "Range");
        report.page.add_inner_button(__("Year"), function() {
            frappe.query_report.get_filter('start_date').set_value(frappe.datetime.year_start());
            frappe.query_report.get_filter('end_date').set_value(frappe.datetime.year_end());
        }, "Range");
    },
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
		},
		{
			'fieldname': 'is_paid',
			'label': __('Paid'),
			'fieldtype': 'Check'
		},
		{
			'fieldname':'group_by_sc',
			'label': __('Group By Service Centre'),
			'fieldtype':'Check',
			'default': 1
		},

	]
};
