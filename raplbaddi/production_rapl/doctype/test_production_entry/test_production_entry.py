# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TestProductionEntry(Document):
	def on_submit(self):
		manufacture({"items": self.items})

@frappe.whitelist()
def manufacture(args):
	"""Helper function to make a Stock Entry
	:items: Item to be moved
	"""
	

	s = frappe.new_doc("Stock Entry")
	args = frappe._dict(args)
	s.company = "Real Appliances Private Limited"
	s.stock_entry_type = "Geyser Manufactured"
	s.purpose = "Manufacture"
	
	# items
	for item in args.items:
		s.append('items', {
			"item_code": item['item_code'],
			"qty": item['qty'],
			"t_warehouse": item['brand'] + " RAPL",
		})

	# insert
	s.insert()
	s.submit()
	return s