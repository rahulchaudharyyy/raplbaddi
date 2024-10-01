import frappe

def validate(doc, method):
    validate_bill_to_ship_to(doc)

def validate_bill_to_ship_to(doc):
    bill_to_ship_to = doc.is_bill_to_ship_to
    billing_gstin = frappe.get_value("Address", doc.customer_address, "gstin")
    shipping_gstin = frappe.get_value("Address", doc.shipping_address_name, "gstin")
    if billing_gstin != shipping_gstin and not bill_to_ship_to:
        frappe.throw(("Please Check Bill To and Ship To if Billing and Shipping GSTIN are not same"))