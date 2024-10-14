from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

custom_fields = {
    "Purchase Order": [
        {
            "is_system_generated": 1,
            "label": "Branch",
            "fieldname": "branch",
            "insert_after": "company",
            "fieldtype": "Link",
            "default": "Real Appliances Private Limited",
            "options": "Branch",
            "reqd": 1,
            "allow_on_submit": 0,
        },
        {
            "is_system_generated": 1,
            "dt": "Purchase Order",
            "label": "Supplier Section Rapl",
            "fieldname": "supplier_section_rapl",
            "insert_after": "based_on_material_request",
            "fieldtype": "Section Break",
            "collapsible": 1,
            "print_hide": 1,
        },
        {
            "is_system_generated": 1,
            "dt": "Purchase Order",
            "label": "Supplier Invoice No",
            "fieldname": "supplier_invoice_no",
            "insert_after": "supplier_section_rapl",
            "fieldtype": "Data",
        },
        {
            "is_system_generated": 1,
            "dt": "Purchase Order",
            "label": "Billing Rule",
            "fieldname": "billing_rule",
            "insert_after": "supplier_invoice_no",
            "fieldtype": "Link",
            "options": "Billing Rule Rapl",
            "no_copy": 0,
            "allow_on_submit": 1,
        },
        {
            "is_system_generated": 1,
            "dt": "Purchase Order",
            "fieldname": "supplier_section_clbrk1",
            "insert_after": "billing_rule",
            "fieldtype": "Column Break",
            "print_hide": 1,
        },
        {
            "is_system_generated": 1,
            "dt": "Purchase Order",
            "label": "Is Billed",
            "fieldname": "is_billed",
            "insert_after": "supplier_section_clbrk1",
            "fieldtype": "Check",
            "default": "1",
            "allow_on_submit": 1,
        },
        {
            "is_system_generated": 1,
            "dt": "Purchase Order",
            "label": "Bill Attachment",
            "fieldname": "bill_attachment",
            "insert_after": "is_billed",
            "fieldtype": "Attach",
            "allow_on_submit": 1,
            "mandatory_depends_on": "eval: doc.is_billed",
        },
        {
            "is_system_generated": 1,
            "dt": "Purchase Order",
            "fieldname": "supplier_section_rapl_2",
            "insert_after": "bill_attachment",
            "fieldtype": "Section Break",
        },
    ],
}


def execute():
    create_custom_fields(custom_fields)
