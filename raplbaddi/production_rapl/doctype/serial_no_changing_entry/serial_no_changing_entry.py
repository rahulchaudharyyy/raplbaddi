# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SerialNoChangingEntry(Document):
	pass
@frappe.whitelist()
def get_production_data(serial_number):
	items = frappe.db.sql(f"""
		SELECT DISTINCT gpet.item_name, gpet.brand, gpe.date_of_production
		FROM `tabGeyser Production Entry Table` as gpet JOIN `tabGeyser Production Entry` as gpe ON gpe.name = gpet.parent
		WHERE '{serial_number}' BETWEEN from_serial AND to_serial
	""", as_dict=True)
	return items