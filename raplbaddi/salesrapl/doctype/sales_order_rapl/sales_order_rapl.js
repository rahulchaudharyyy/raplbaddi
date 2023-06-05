// Copyright (c) 2023, Nishant Bhickta and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Order Rapl', {
	refresh: function (frm) {
		frm.add_custom_button(("Create Sales Order"), function () {
			frappe.new_doc('Sales Order', {
				"customer": frm.doc.customer,
				"sales_order_rapl": frm.doc.name
			})
			
		});
	},
	delivery_date: function(frm){
		console.log(frm.doc.delivery_date)
	}
});


frappe.ui.form.on("Sales Order", {
    "refresh": function(frm, cdt, cdn) {
        if(frm.doc.__islocal && frm.doc.sales_order_rapl){
            frappe.model.with_doc("Sales Order Rapl", frm.doc.sales_order_rapl, function() {
                var mcd = frappe.model.get_doc("Sales Order Rapl", frm.doc.sales_order_rapl);
                cur_frm.clear_table("items");
                    $.each(mcd.items, function(i, d) {
                        i = frm.add_child("items");
                        i.item_code = d.geyser;
                        i.delivery_date = d.date_expected;
                        i.qty = d.qty;
                    });
                cur_frm.refresh_field("items");
            });
        }
    }	
});


frappe.ui.form.on("Sales Order Items")


// i.item_name = d.item_name;
// i.product_make = d.product_make;
// i.cas_no = d.cas_no;
// i.uom = d.uom;
// i.stock_uom = d.uom;
// i.description = d.description;
// i.qty = d.qty;

frappe.ui.form.on('Sales Order', {
    customer: function(frm){
        console.log(frm.doc.sale_order_item_boxes)
    }
})


frappe.ui.form.on('Sales Order Item', {
	item_code: function(frm) {
        console.log(frm)
    }
})