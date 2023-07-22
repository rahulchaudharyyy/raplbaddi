// Copyright (c) 2023, Nishant Bhickta and contributors
// For license information, please see license.txt
frappe.ui.form.on('Testing Report', {
	onload(frm) {
		// frm.get_field("items").grid.cannot_add_rows = true;

		frm.set_query("department", function (doc) {
			return {
				filters: {
					parent_department: "Testing - RAPL"
				}
			};
		});
	},
	department(frm) {
		let department_map = {
			"Element : T - RAPL": "Element Unit",
			"Tank: T - RAPL": "Tank Metal",
			"Paintshop : T - RAPL": "Geyser Unit",
		};

		let department = frm.doc.department;
		let itemGroup = department_map[department] || "";

		frm.set_query("item", function (doc) {
			return {
				filters: {
					item_group: itemGroup
				}
			};
		});
	},
	fetch_parameters(frm) {
		frappe.db.get_value('Department', frm.doc.department, 'abbriviation').then(r => {
			let abb = r.message.abbriviation
			frappe.db.get_list('Testing Parameters').then(
				r => {
					r.forEach(i => {
						if (i.name.includes(abb) && frm.doc.item_name) {
							frm.add_child('items', { parameter: i.name, item: frm.doc.item_name, item_code: frm.doc.item })
						}
					})
					frm.refresh_field('items')
					frm.set_value('item', '')
					frm.refresh_field('item')
				}
			)
		})
	}
});
