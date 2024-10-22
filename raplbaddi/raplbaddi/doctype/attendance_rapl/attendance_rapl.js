// Copyright (c) 2024, Nishant Bhickta and contributors
// For license information, please see license.txt

frappe.ui.form.on("Attendance Rapl", {
    onload: function(frm) {
        if(!frm.doc.docstatus) {
            fill_items_onload(frm)
        }
    },
});

function fill_items_onload(frm) {
    frappe.call({
        method: 'raplbaddi.raplbaddi.doctype.attendance_rapl.attendance_rapl.get_employee_shift_info',
        frm: frm,
        callback: function(response) {
            if (response.message) {
                frm.clear_table('items');
                response.message.forEach(info => {
                    const row = frm.add_child('items');
                    row.employee = info.employee;
                    row.employee_name = info.employee_name;
                    row.shift_type = info.default_shift;
                    row.check_in = info.start_time;
                    row.check_out = info.end_time;
                });
                frm.refresh_field('items');
            }
        }
    });
}
