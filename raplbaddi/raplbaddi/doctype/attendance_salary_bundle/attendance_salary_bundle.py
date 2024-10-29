# Copyright (c) 2024, Nishant Bhickta and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AttendanceSalaryBundle(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from raplbaddi.raplbaddi.doctype.attendance_salary_bundle_item.attendance_salary_bundle_item import AttendanceSalaryBundleItem

		amended_from: DF.Link | None
		employee: DF.Link | None
		items: DF.Table[AttendanceSalaryBundleItem]
		total_holiday: DF.Float
		total_salary: DF.Float
	# end: auto-generated types
	pass

	def on_trash(self):
		pass