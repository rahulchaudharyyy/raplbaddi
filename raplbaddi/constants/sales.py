from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

custom_fields = {
    "Sales Order Item": [
        {
            "is_system_generated": 1,
            "label": "Color",
            "fieldname": "color",
            "insert_after": "delivery_date",
            "fieldtype": "Link",
            "default": "Regular",
            "options": "Color",
            "reqd": 0,
            "allow_on_submit": 1,
            "in_list_view": 1,
            "columns": 1,
            "reqd": 1,
        }
    ],
    "Delivery Note": [
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
            "label": "Driver Number",
            "fieldname": "driver_number",
            "insert_after": "lr_date",
            "fieldtype": "Int",
            "reqd": 1,
            "allow_on_submit": 0,
        },
        {
            "is_system_generated": 1,
            "label": "Bilty/LR No,",
            "fieldname": "bilty_no",
            "insert_after": "driver_number",
            "fieldtype": "Data",
            "reqd": 1,
            "allow_on_submit": 0,
        },
    ],
}


def execute():
    create_custom_fields(custom_fields)
