# Copyright (c) 2024, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


class AttendanceRapl(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from raplbaddi.raplbaddi.doctype.attendance_rapl_item.attendance_rapl_item import AttendanceRaplItem

		amended_from: DF.Link | None
		date: DF.Date
		items: DF.Table[AttendanceRaplItem]
	# end: auto-generated types
	pass

@frappe.whitelist()
def get_employee_shift_info():
	employees = frappe.get_all('Employee', fields=['name', 'employee_name', 'default_shift'])
	shift_info = []

	for employee in employees:
		shift = frappe.get_value('Shift Type', employee.default_shift, ['start_time', 'end_time'])
		if shift:
			start_time = shift[0]
			end_time = shift[1]

			shift_info.append({
				'employee': employee.name,
				'employee_name': employee.employee_name,
				'default_shift': employee.default_shift,
				'start_time': start_time,
				'end_time': end_time,
			})

	return shift_info