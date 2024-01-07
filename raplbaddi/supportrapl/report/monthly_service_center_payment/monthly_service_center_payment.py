# Copyright (c) 2024, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe

class payment:
    def __init__(self, filters) -> None:
        self.get_data()
        self.filters = filters
        self.process_filters()

    def process_filters(self):
        if self.filters.months:
            self.filters.month_code = int(
                frappe.get_value("Months", self.filters.months, "month_code")
            )

    def get_data(self):
        query = f"""
        select 
            COUNT(i.name) as 'count',
            CASE WHEN i.custom_creation_date THEN i.custom_creation_date ELSE i.creation END as 'date',
            j.service_centre_name as 'service_centre',
            j.bank_name as 'bank',
            j.bank_account_no as 'account_no',
            j.ifsc_code as 'ifsc',
            j.upi_id as 'upi',
            sum(i.amount) as 'amount'
        from tabIssueRapl as i
            left Join
            `tabService Centre` as j on i.service_centre = j.service_centre_name
        where
            i.service_delivered = 'Yes'
        group by
            i.service_centre
        order by
            amount DESC, count DESC
        """

        result = frappe.db.sql(query, as_dict=True)
        self.data = result

    def filtered_data(self):
        self.filtered_data = []
        for data in self.data:
            data.month_code = data.date.month
            data.date = data.date.date()
            data.amount = int(data.amount)
            data.ifsc = data.ifsc.upper()
            data.per_complaint = int(data.amount/data.count)
            if (
                (not self.filters.month_code or data.month_code == self.filters.month_code) and
                (not self.filters.service_centre or data.service_centre == self.filters.service_centre)
            ):
                self.filtered_data.append(data)
        return self.filtered_data

    def get_columns(self):
        columns = [
            # {"fieldname": "date", "label": ("date"), "fieldtype": "date", "width": 300},
            {
                "fieldname": "service_centre",
                "label": ("Service Centre"),
                "fieldtype": "Link",
                "options": "Service Centre",
                "width": 300,
            },
            {
                "fieldname": "bank",
                "label": ("Bank Name"),
                "fieldtype": "Data",
                "width": 137,
            },
            {
                "fieldname": "account_no",
                "label": ("Account No"),
                "fieldtype": "Data",
                "width": 137,
            },
            {
                "fieldname": "ifsc",
                "label": ("IFSC Code"),
                "fieldtype": "Data",
                "width": 137,
            },
            {"fieldname": "upi", "label": ("upi"), "fieldtype": "Data", "width": 137},
            {
                "fieldname": "amount",
                "label": ("Amount"),
                "fieldtype": "int",
                "width": 137,
            },
            {
                "fieldname": "count",
                "label": ("Count"),
                "fieldtype": "int",
                "width": 137,
            },
          {
                "fieldname": "per_complaint",
                "label": ("Per Complaint"),
                "fieldtype": "int",
                "width": 137,
            },
        ]
        return columns

    def get_msg(self):
        pass


def execute(filters=None):
    payee = payment(filters)
    columns, data = [], []
    return payee.get_columns(), payee.filtered_data()


# {'fieldname': 'complaint_no','label': ('Complaint No.'),'fieldtype': 'Link','options':'IssueRapl','width':300},
