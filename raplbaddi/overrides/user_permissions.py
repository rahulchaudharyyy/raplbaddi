import frappe

def validate(doc, method):
    if not frappe.session.user == "Administrator":
        frappe.throw(f"User <b>User Access Control Instead</b> to edit user access")