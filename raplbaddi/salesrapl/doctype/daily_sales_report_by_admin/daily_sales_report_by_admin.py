# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class DailySalesReportByAdmin(Document):
	def validate(self):
		amt = self.amount_for_travel
		for x in self.daily_sales_expenses_by_admin:
			amt += x.amount
		self.total_amount = amt
