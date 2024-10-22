// Copyright (c) 2024, Nishant Bhickta and contributors
// For license information, please see license.txt

frappe.ui.form.on("Attendance Rapl", {
    onload: function(frm) {
        if(!frm.doc.docstatus) {
            frm.events.fill_items_onload(frm)
        }
    },
    fill_items_onload(frm) {
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Employee',
                fields: ['name', 'employee_name']
            },
            callback: function(response) {
                if (response.message) {
                    const employees = response.message;
                    frm.clear_table('items');
                    employees.forEach(employee => {
                        const row = frm.add_child('items');
                        row.employee = employee.name;
                        row.employee_name = employee.employee_name;
                    });
                    frm.refresh_field('items');
                }
            }
        });
    }
});
