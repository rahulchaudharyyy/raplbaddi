import frappe

@frappe.whitelist()
def get_customer_details(customer):
    address = frappe.db.sql(f"""
        SELECT customer_address, customer_phone
        FROM `tabSupport Customer`
        WHERE customer_name='{customer}'
    """, as_dict=True)
    return address