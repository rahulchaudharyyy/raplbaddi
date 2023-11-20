# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from .maps import GoogleMapClient

mapclient = GoogleMapClient()


class IssueRapl(Document):
    def get_sc_address(self):
        service_centres = frappe.get_all(
            "Service Centre",
            ["state", "district", "pincode", "address", "name"],
            filters={"state": self.state},
        )
        service_centres = [
            {entry["name"]: " ".join([entry[k] for k in entry if k != "name"]).strip()}
            for entry in service_centres
        ]
        sc_addresses = []
        for sc in service_centres:
            for v in sc.values():
                sc_addresses.append(v)
        return sc_addresses

    def get_customer_address(self):
        customer_address = " ".join(
            [self.state, self.district, self.pin_code, self.customer_address]
        )
        return customer_address

    def validate(self):
        self.get_sc_address()
        # self._get_rates()

    def _get_rates(self, service_centre=None):
        rates = frappe.get_all(
            "Service Centre",
            ["kilometer_category", "fixed_rate", "per_kilometer_rate"],
            filters={"name": self.service_centre if not service_centre else service_centre},
        )[0]
        kilometer_category, fixed_rate, per_kilometer_rate = (
            rates.get("kilometer_category"),
            rates.get("fixed_rate"),
            rates.get("per_kilometer_rate"),
        )
        rate = float(fixed_rate) + float(per_kilometer_rate) * float(self.kilometer)
        self.amount = rate
        return rate

    @frappe.whitelist()
    def get_addresses(self):
        distances = mapclient.get_distance(
            self.get_customer_address(), self.get_sc_address()
        )
        return distances[0:6]

    @frappe.whitelist()
    def set_rates(self):
        issues = frappe.get_all('IssueRapl')
        for issue in issues:
            name = issue.get('name')
            doc = frappe.get_doc('IssueRapl', name)
            doc.amount = self._get_rates(service_centre=doc.service_centre)
            print(doc.amount)
            doc.save()
        frappe.msgprint('Amounts has been set in all issues')