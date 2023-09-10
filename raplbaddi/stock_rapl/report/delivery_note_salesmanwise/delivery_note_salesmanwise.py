# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt
import frappe

def execute(filters=None):
    columns, data = [], []
    data = get_data(filters)
    return get_columns(filters), data

def get_data(filters):
    query = f"""
        SELECT DISTINCT
            dn.name as dn,
            dn.customer_name as customer_name,
            dn.posting_date as posting_date,
            dn.total_qty as total_qty,
            dni.uom as uom,
            cu.customer_group as customer_group,
            GROUP_CONCAT(DISTINCT dni.item_name) as items
        FROM
            `tabDelivery Note` as dn
            LEFT JOIN `tabCustomer` as cu ON dn.customer_name = cu.customer_name
            LEFT JOIN `tabDelivery Note Item` as dni ON dni.parent = dn.name
        WHERE {get_conditions(filters)}
        GROUP BY
            dn.name
        ORDER BY
            dn.posting_date DESC, dn.posting_time DESC
    """
    result = frappe.db.sql(query, as_dict=True)
    return result

def get_columns(filters):
    columns = [
        {"label": "Customer", "fieldname": "customer_name", "fieldtype": "Link", "options": "Customer", "width": 250},
        {"label": "Delivery Note", "fieldname": "dn", "fieldtype": "Link", "options": "Delivery Note", "width": 150},
        {"label": "Delivery Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": "Quantity", "fieldname": "total_qty", "fieldtype": "Int", "width": 50},
        {"label": "Unit", "fieldname": "uom", "fieldtype": "Data", "width": 50},
        {"label": "Name", "fieldname": "items", "fieldtype": "Data", "width": 150},
        {"label": "Salesman", "fieldname": "customer_group", "fieldtype": "Data", "width": 50},
    ]
    return columns

def get_conditions(filters):
    conditions = "dn.posting_date >= '2023-08-19' AND dn.docstatus = 1"
    if filters and filters.get("from_date"):
        from_date = filters.get("from_date")
        conditions += f" AND dn.posting_date >= '{from_date}'"
    if filters and filters.get("to_date"):
        to_date = filters.get("to_date")
        conditions += f" AND dn.posting_date <= '{to_date}'"
    if filters and filters.get("sales_person"):
        sales_person = filters.get("sales_person")
        conditions += f" AND cu.customer_group = '{sales_person}'"
    return conditions