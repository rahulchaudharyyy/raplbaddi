# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    return get_columns(filters), get_data(filters)


def get_columns(filters):
    columns = [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 100},
        {"label": "Date", "fieldname": "audit", "fieldtype": "Date", "width": 100},
        {"label": "Type", "fieldname": "type", "fieldtype": "Data", "width": 180},
        {"label": "Amount", "fieldname": "amount",
            "fieldtype": "Currency", "width": 150},
    ]
    return columns


def get_amount(filters):
    if filters and filters.get("group_by_expense_type"):
        return 'SUM(dse.amount)'
    else:
        return 'dse.amount'


def get_data(filters):
    query = f"""
    SELECT
        dsr.date, dse.type, {get_amount(filters)} as amount, dsr.amount_for_travel, dsr.audit
    FROM
        `tabDaily Sales Report By Admin` as dsr
        JOIN
        `tabDaily Sales Expenses By Admin` as dse ON dse.parent = dsr.name
    WHERE
        {get_conditions(filters)}
    {get_group(filters)}
    """
    result = frappe.db.sql(query, as_dict=True)
    unique_data = {}
    for item in result:
        date = item['date']
        amount = item.pop('amount_for_travel')
        if date not in unique_data:
            unique_data[date] = amount

    amount_append = []
    for date, amount_for_travel in unique_data.items():
        d = {
            "date": date,
            "type": "Travel",
            "amount": amount_for_travel
        }
        amount_append.append(d)
    result.extend(amount_append)
    return result


def get_conditions(filters):
    conditions = "1"
    if filters and filters.get("sales_person"):
        sales_person = filters.get("sales_person")
        conditions += f" AND dsr.sales_person = '{sales_person}'"
    if filters and filters.get("start_date"):
        start_date = filters.get("start_date")
        conditions += f" AND dsr.date >= '{start_date}'"
    if filters and filters.get("end_date"):
        end_date = filters.get("end_date")
        conditions += f" AND dsr.date <= '{end_date}'"
    return conditions


def get_group(filters):
    ret = "GROUP BY "
    if filters and filters.get("group_by_expense_type"):
        ret += "dse.type"
    else:
        ret = ""
    return ret
