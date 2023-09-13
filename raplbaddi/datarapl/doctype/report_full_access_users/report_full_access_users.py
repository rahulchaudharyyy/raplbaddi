# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ReportFullAccessUsers(Document):
	pass

def get_wildcard_users():
    users= frappe.get_all(
			"Report Full Access Users",
			fields=["user", "check"]
		)
    wildcard_users = [user['user'] for user in users]
    wildcard_users.append('Administrator')
    return wildcard_users