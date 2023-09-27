# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ElementEntry(Document):
    def on_submit(self):
        issue(
            items=self.get("items"),
            name=self.get("name"),
            date=self.get("date_of_entry"),
            entry_type=self.get("entry_type"),
        )


@frappe.whitelist()
def issue(items, name, date, entry_type):
    """Helper function to make a Stock Entry
    :items: Item to be moved
    """
    s = frappe.new_doc("Stock Entry")
    s.company = "Real Appliances Private Limited"

    entry_map = {
        "Issue": "Element Issue",
        "Receipt": "Element Receipt",
        "Rework": "Element Receipt",
    }

    s.stock_entry_type = entry_map[entry_type]
    s.element_entry = name
    s.set_posting_time = 1
    s.posting_date = date

    # items
    for item in items:
        t_warehouse = (
            "Element Section - RAPL" if entry_type == "Element Receipt" else ""
        )
        s_warehouse = (
            "Stores - RAPL"
            if entry_type == "Element Receipt"
            else "Element Section - RAPL"
        )
        s.append(
            "items",
            {
                "item_code": item.item,
                "qty": item.qty,
                "t_warehouse": t_warehouse,
                "s_warehouse": s_warehouse,
                "is_finished_item": 1,
            },
        )
    # insert
    s.insert()
    s.submit()
    return s
