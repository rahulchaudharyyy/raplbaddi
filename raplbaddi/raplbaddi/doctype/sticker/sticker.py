# Copyright (c) 2024, Nishant Bhickta and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Sticker(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		sample: DF.AttachImage | None
		sticker_type: DF.Literal["", "Logo", "Lahar", "ISI", "Specification Plate", "Five Star", "Box Model Sticker"]
		title: DF.Data
	# end: auto-generated types
	pass
