# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from .maps import GoogleMapClient
from frappe.model.document import Document

mapclient = GoogleMapClient()


class IssueRapl(Document):
    def autoname(self):
        pass

    def get_sc_addresses(self):
        service_centres = frappe.get_all(
            "Service Centre",
            ["state", "district", "pincode", "address", "name"],
            filters={"state": self.customer_address_state},
        )

        sc_addresses = []

        for entry in service_centres:
            components = [
                str(entry[k]) for k in entry if k != "name" and entry[k] is not None
            ]
            address = " ".join(components).strip()
            formatted_entry = f"{entry['name']}: {address}"
            sc_addresses.append(formatted_entry)

        return sc_addresses

    def get_customer_address(self):
        return self.customer_address

    def validate(self):
        self.get_sc_addresses()
        self.amount = self._get_rates()

    def _get_rates(self, service_centre=None):
        rates = frappe.get_all(
            "Service Centre",
            ["kilometer_category", "fixed_rate", "per_kilometer_rate", "per_kilometer_rate_for_2", "per_kilometer_rate_for_3_or_more",],
            filters={
                "name": self.service_centre if not service_centre else service_centre
            },
        )[0]
        (
            kilometer_category,
            fixed_rate,
            per_kilometer_rate,
            per_kilometer_rate_for_2,
            per_kilometer_rate_for_3_or_more,
        ) = (
            rates.get("kilometer_category"),
            rates.get("fixed_rate"),
            rates.get("per_kilometer_rate"),
            rates.get("per_kilometer_rate_for_2"),
            rates.get("per_kilometer_rate_for_3_or_more"),
        )
        net_kilometer = max(0, float(self.kilometer) - float(kilometer_category))
        extra_pcs_rate = 0
        if self.no_of_pcs == 2:
            extra_pcs_rate = per_kilometer_rate_for_2
        elif self.no_of_pcs > 2:
            extra_pcs_rate = per_kilometer_rate_for_3_or_more
        final_rate = (
            float(fixed_rate)
            + (extra_pcs_rate * (self.no_of_pcs - 1))
            + (float(per_kilometer_rate) * float(net_kilometer))
            + self.extra_cost
        )
        print(final_rate)
        final_rate = self.no_of_visits * final_rate
        return final_rate

    @frappe.whitelist()
    def get_addresses(self):
        distances = mapclient.get_distance(
            self.get_customer_address(), self.get_sc_addresses()
        )
        return distances[0:6]

    @frappe.whitelist()
    def set_rates(self):
        issues = frappe.get_all("IssueRapl")
        for issue in issues:
            name = issue.get("name")
            doc = frappe.get_doc("IssueRapl", name)
            doc.amount = self._get_rates(service_centre=doc.service_centre)
            doc.save()
        frappe.msgprint("Amounts has been set in all issues")
