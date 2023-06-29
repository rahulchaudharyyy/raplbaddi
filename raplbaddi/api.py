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

@frappe.whitelist()
def price_list_of_customer(customer=None):
    try:
        price_list = frappe.db.sql(f"""
            SELECT soi.item_code, soi.rate, soi.discount_amount, MAX(so.transaction_date) AS latest_transaction_date
            FROM `tabSales Order Item` AS soi
            JOIN `tabSales Order` AS so ON so.name = soi.parent
            WHERE so.customer = '{customer}' AND so.docstatus = 1
            GROUP BY so.customer, soi.item_code
        """, as_dict=True
        )
        return price_list
    except:
        return "Doc not found"