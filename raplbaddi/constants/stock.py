from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

custom_fields = {
    "Item": [
        {
            "name": "Item-unit",
            "label": "Unit",
            "fieldname": "unit",
            "insert_after": "over_billing_allowance",
            "fieldtype": "Select",
            "options": "Unit 1\nUnit 2"
        }
    ]
}


def execute():
    create_custom_fields(custom_fields)
