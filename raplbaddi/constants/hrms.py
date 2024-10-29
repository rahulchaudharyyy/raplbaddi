from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

custom_fields = {
    "Shift Type": [
        {
            "is_system_generated": 1,
            "label": "Time Allowance",
            "fieldname": "time_allowance",
            "insert_after": "end_time",
            "fieldtype": "Float",
            "description": "In Seconds",
            "default": 900,
            "read_only": 0,
            "hidden": 0,
            "no_copy": 0,
        },
        {
            "is_system_generated": 1,
            "label": "Has Overtime",
            "fieldname": "has_overtime",
            "insert_after": "time_allowance",
            "fieldtype": "Check",
            "read_only": 0,
            "hidden": 0,
            "no_copy": 0,
        },
    ]
}

def execute():
    create_custom_fields(custom_fields)