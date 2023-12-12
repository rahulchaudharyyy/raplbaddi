// Copyright (c) 2023, Nishant Bhickta and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Sales Report By Admin', {
	km_travelled(frm) {
		let doc = frm.doc
		frm.set_value('amount_for_travel', doc.km_travelled * 8)
		frm.refresh_field('amount_for_travel')
	},
	end_reading(frm) {
		let doc = frm.doc
		if (doc.end_reading && doc.start_reading) {
			let km_travelled = doc.end_reading - doc.start_reading
			if (km_travelled >= 1) {
				frm.set_value('km_travelled', km_travelled)
				frm.refresh_field('km_travelled')
			} else {
				frm.set_value('km_travelled', 0)
				frm.set_value('end_reading', 0)
				frm.refresh_field('km_travelled')
				frm.refresh_field('end_reading')
				frappe.throw('Start reading must be less than end reading...')
			}
		}
	}
});
