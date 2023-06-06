import frappe

@frappe.whitelist()
def get_customer_details(customer):
    return frappe.db.sql(f"""
        SELECT customer_address, customer_phone_number, serial_no, brand, model
        FROM `tabSupport Customer`
        WHERE name='{customer}'
    """, as_dict=True)

@frappe.whitelist()
def get_dpi_parent(sno):
       return frappe.db.sql(f"""
        SELECT parent FROM `tabDaily Production Item` as dpi
        WHERE dpi.name='{sno}'
    """, as_dict=True)

@frappe.whitelist()
def get_last_so_of_customer(customer=None):
    filter =  {'customer': customer}
    try:
        so = frappe.get_last_doc('Sales Order', filters=filter)
        return so
    except:
        return "Doc not found"
