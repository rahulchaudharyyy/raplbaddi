// Copyright (c) 2023, Nishant Bhickta and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Test Production Entry', {
// 	refresh: function(frm) {

// 	}
// });

// frappe.ui.form.on('Test Production Entry Table', {
// 	to_serial(frm, cdt, cdn) {
// 		calculate_qty(frm, cdt, cdn)
// 	},

// 	before_submit(frm) {

// 		frappe.call({
// 			method: "erpnext.stock.doctype.stock_entry.stock_entry_utils.make_stock_entry",
// 			args: {
// 				items: str,
// 				qty: frm.,
// 				company: "Real Appliances Private Limited",
// 				to_warehouse: frm.doc.brand + " - RAPL",
// 				purpose: "Manufacture",
// 				do_not_save: bool = False,
// 				do_not_submit: bool = False,
// 				inspection_required: bool = False,
// 			}
// 		})


// );

// function calculate_qty(frm, cdt, cdn) {
// 	let row = locals[cdt][cdn];
// 	if (row.to_serial - row.from_serial + 1) {
// 		frappe.model.set_value(cdt, cdn, 'qty', row.to_serial - row.from_serial + 1);
// 	} else {
// 		frappe.throw("Qty should be 1 or Above")
// 		frappe.model.set_value(cdt, cdn, 'qty', 0);
// 	}
// 	if (!(row.qty > 0)) {
// 		frappe.throw("Qty should be 1 or Above")
// 		frappe.model.set_value(cdt, cdn, 'qty', 0);

// 	}
// }