# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt
import frappe
from frappe.core.doctype.user_permission.user_permission import get_user_permissions
from raplbaddi.datarapl.doctype.report_full_access_users.report_full_access_users import get_wildcard_users

def get_groups(user):
    user_permissions = get_user_permissions(user=user)
    allowed_groups = [groups['doc'] for groups in user_permissions.get('Customer Group', [])]
    return allowed_groups

def permissions(filters):
    user = frappe.session.user
    if filters.get('sales_person') in get_groups(user) or user in get_wildcard_users():
        return True
    if filters.get('sales_person') == 'All' and user in get_wildcard_users():
        return True
    else:
        return False

def execute(filters=None):
    columns, data = [], []
    if permissions(filters):
        data = get_data(filters)
        return get_columns(filters), data
    else:
        return None

def get_data(filters):
    query = f"""
        SELECT
            customer,
            salesman,
            SUM(net_sales) AS net_sales
        FROM (
            SELECT
                SUM(IF(td.transaction_type = 'Sales', td.quantity, -(td.quantity))) AS net_sales,
                tp.customer AS customer,
                cu.customer_group AS salesman,
                td.date AS date
            FROM
                `tabTally April to August 2023` AS td
                LEFT JOIN `tabTally Party Name` AS tp ON td.party_name = tp.name
                LEFT JOIN `tabTally Particular` as tr ON td.particulars = tr.name
                LEFT JOIN `tabCustomer` AS cu ON tp.customer = cu.name
                LEFT JOIN `tabItem` as i ON i.name = tr.item
            WHERE
                td.date BETWEEN '2023-04-01' AND '2023-08-28'
                AND i.item_group = 'Geyser Unit'
            GROUP BY
                tp.customer

            UNION
            
            SELECT
                SUM(dni.qty) AS net_sales,
                dn.customer_name AS customer,
                cu.customer_group AS salesman,
                dn.posting_date AS date
            FROM
                `tabDelivery Note` AS dn
                LEFT JOIN `tabDelivery Note Item` AS dni ON dni.parent = dn.name
                LEFT JOIN `tabCustomer` AS cu ON dn.customer_name = cu.customer_name
<<<<<<< Updated upstream
=======
                LEFT JOIN `tabDelivery Note Item` as dni ON dni.parent = dn.name
>>>>>>> Stashed changes
                LEFT JOIN `tabItem` as i ON dni.item_code = i.name
            WHERE
                dn.posting_date >= '2023-08-29'
                AND dn.docstatus = 1
                AND i.item_group = 'Geyser Unit'
            GROUP BY
                dn.customer_name
            HAVING
                MAX(dn.posting_date) >= '2023-08-29'
        ) AS d
        WHERE {get_conditions(filters)}
        GROUP BY
            d.customer
        ORDER BY
            net_sales DESC
    """

    result = frappe.db.sql(query, as_dict=True)
    return result


def get_columns(filters):
    columns = [
        {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 250,
        },
        {
            "label": "Net Sales",
            "fieldname": "net_sales",
            "fieldtype": "Int",
            "width": 120,
        }
    ]
    return columns


def get_conditions(filters):
    conditions = "net_sales > 0"
    if filters and filters.get("from_date"):
        from_date = filters.get("from_date")
        conditions += f" AND d.date >= '{from_date}'"
    if filters and filters.get("to_date"):
        to_date = filters.get("to_date")
        conditions += f" AND d.date <= '{to_date}'"
    if filters and filters.get("sales_person"):
        sales_person = filters.get("sales_person")
        if sales_person == 'All':
            conditions += f" AND 1"
        else:
            conditions += f" AND d.salesman = '{sales_person}'"
    return conditions
