# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class BillingRuleRapl(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		applicable_for: DF.Literal["", "Both", "Buying", "Selling"]
		description: DF.Text | None
		disabled: DF.Check
		title: DF.Data | None
	# end: auto-generated types
	pass

	