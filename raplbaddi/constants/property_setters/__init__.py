import frappe
from ..sales import property_setters as selling_property_setters

property_setters = []

for ps in [selling_property_setters, ]:
    property_setters.extend(ps)

def execute():
    for ps in property_setters:
        try:
            doc = frappe.get_doc("Property Setter", ps.get('name'))
            doc.update(ps)
            doc.save()
        except frappe.exceptions.DoesNotExistError as e:
            doc = frappe.get_doc(ps)
            doc.insert()