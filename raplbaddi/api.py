import frappe

@frappe.whitelist()
def get_customer_details(customer):
    return frappe.db.sql(f"""
        SELECT customer_address, customer_phone_number, serial_no, brand, model
        FROM `tabSupport Customer`
        WHERE name='{customer}'
    """, as_dict=True)