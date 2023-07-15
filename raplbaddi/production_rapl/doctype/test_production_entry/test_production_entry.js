// Copyright (c) 2023, Nishant Bhickta and contributors
// For license information, please see license.txt

frappe.ui.form.on('Test Production Entry Table', {
	to_serial(frm, cdt, cdn) {
		calculate_qty(frm, cdt, cdn)
	}
});

function calculate_qty(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	if (row.to_serial - row.from_serial + 1) {
		frappe.model.set_value(cdt, cdn, 'qty', row.to_serial - row.from_serial + 1);
	} else {
		frappe.throw("Qty should be 1 or Above")
		frappe.model.set_value(cdt, cdn, 'qty', 0);
	}
	if (!(row.qty > 0)) {
		frappe.throw("Qty should be 1 or Above")
		frappe.model.set_value(cdt, cdn, 'qty', 0);

	}
}