// Copyright (c) 2023, Nishant Bhickta and contributors
// For license information, please see license.txt

frappe.ui.form.on('Serial No Changing Entry', {
	before_save(frm){
		frm.set_value('qty', frm.doc.items.length)
	}
});
