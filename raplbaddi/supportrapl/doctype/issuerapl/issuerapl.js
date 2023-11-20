// Copyright (c) 2023, Nishant Bhickta and contributors
// For license information, please see license.txt
frappe.ui.form.on('IssueRapl', {
	refresh: function (frm) {
		frm.add_custom_button(__('Set Rates in All Issues'), function () {
			frm.call({
				method: 'set_rates',
				doc: frm.doc,
				callback: function (response) {
				}
			})
		})
		frm.add_custom_button(__('Select SC'), function () {
			frm.call({
				method: 'get_addresses',
				doc: frm.doc,
				callback: function (response) {
					if (response.message) {
						var options = response.message;
						frappe.prompt({
							label: __('Select an Address'),
							fieldname: 'selected_address',
							fieldtype: 'Select',
							options: options,
							reqd: 1,
						},
							(values) => {
								value = values.selected_address.split(':')
								frm.set_value('service_centre', value[1])
								frm.set_value('kilometer', value[0])
							});
					}
				}
			});
		});
	}
});

