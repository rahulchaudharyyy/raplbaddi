# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt
import frappe

def execute(filters=None):
    columns, data = [], []
    data = get_data(filters)
    return get_columns(filters), data

def get_data(filters):
    query = f"""
        SELECT
			so.transaction_date as date,
			GROUP_CONCAT(DISTINCT CONCAT('<a href="https://raplbaddi.com/app/sales-order/', so.name, '">', so.name, '</a>')) AS sales_orders,
			so.sales_person as salesman,
			cu.customer_group as customer_group,
			IF(so.delivery_date='2023-12-31' OR so.delivery_date < NOW(), IF(so.status = 'On Hold', 'Hold', 'Current'), DATE_FORMAT(so.delivery_date, '%d/%b/%Y')) as delivery_date,
			so.customer AS `customer`,
			GROUP_CONCAT(DISTINCT soi.name_of_brand) AS `brand`,
		--    GROUP_CONCAT(DISTINCT soi.item_code, "-", soi.name_of_brand) as `Item-Brand`,
			SUM(soi.qty - soi.delivered_qty) AS `orders`,
			CONVERT(SUM(IF(
				( IF(b.actual_qty < 0, 0, b.actual_qty) / (soi.qty - soi.delivered_qty)) * 100 > 100,
				100,
				IF(
					( IF(b.actual_qty < 0, 0, b.actual_qty) / (soi.qty - soi.delivered_qty)) * 100 < 0,
					0,
					CONVERT(( IF(b.actual_qty < 0, 0, b.actual_qty) / (soi.qty - soi.delivered_qty)) * 100, UNSIGNED)
				)
			))/COUNT(soi.item_name), UNSIGNED) as '%%:Int:80',
			SUM(IF((soi.qty - soi.delivered_qty) -  IF(b.actual_qty < 0, 0, b.actual_qty) <= 0, 0, (soi.qty - soi.delivered_qty) -  IF(b.actual_qty < 0, 0, b.actual_qty))) as `shortage`,
			so.conditions as 'remarks',
			so.shipping_address as `shipping_address`
		FROM
			`tabSales Order` so
		JOIN
			`tabSales Order Item` soi ON soi.parent = so.name
		LEFT JOIN
			`tabBin` AS b ON b.item_code = soi.item_code AND b.warehouse = soi.warehouse
		LEFT JOIN
			`tabCustomer` as cu ON cu.name = so.customer_name
		WHERE {get_conditions(filters)}
		GROUP BY so.customer_name, delivery_date, so.shipping_address
		ORDER BY delivery_date, `shortage` ASC, `%%:Int:80` DESC
    """
    result = frappe.db.sql(query, as_dict=True)
    return result

def get_columns(filters):
    columns = [
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 250},
        {"label": "Sales Orders", "fieldname": "sales_orders", "fieldtype": "Data", "options": "Sales Order", "width": 150},
        {"label": "Order Date", "fieldname": "date", "fieldtype": "Date", "width": 100},
        {"label": "Delivery Date", "fieldname": "delivery_date", "fieldtype": "Data", "width": 100},
        {"label": "Orders", "fieldname": "orders", "fieldtype": "Int", "width": 50},
        {"label": "Brand", "fieldname": "brand", "fieldtype": "Data", "width": 50},
        {"label": "Shipping", "fieldname": "shipping_address", "fieldtype": "Data", "width": 150},
        {"label": "Salesman", "fieldname": "customer_group", "fieldtype": "HTML", "width": 50},
		{"label": "Shipping", "fieldname": "remarks", "fieldtype": "Data", "width": 150},
    ]
    return columns

def get_conditions(filters):
    conditions = "so.status NOT IN ('Stopped', 'Closed') AND so.docstatus = 1 AND (soi.qty - soi.delivered_qty) > 0"
    if filters and filters.get("from_date"):
        from_date = filters.get("from_date")
        conditions += f" AND so.transaction_date >= '{from_date}'"
    if filters and filters.get("to_date"):
        to_date = filters.get("to_date")
        conditions += f" AND so.transaction_date <= '{to_date}'"
    if filters and filters.get("sales_person"):
        sales_person = filters.get("sales_person")
        conditions += f" AND cu.customer_group = '{sales_person}'"
    return conditions