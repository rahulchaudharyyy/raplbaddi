# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from raplbaddi.utils import report_utils
from pypika.functions import Abs, Sum
from pypika import Case, CustomFunction

Base = CustomFunction('Greatest', ['default', 'value'])

def execute(filters=None):
	columns, data = [], []
	return get_columns(filters), get_data(filters)

def get_sales_order_data(filters):
	so = frappe.qb.DocType('Sales Order')
	soi = frappe.qb.DocType('Sales Order Item')
	query = (
		frappe.qb
		.from_(so)
		.left_join(soi).on(so.name == soi.parent)
		.where(so.status.notin(['Stopped', 'Closed']) & so.docstatus == 1)
		.where(soi.item_group == "Geyser Unit")
		.where(so.delivery_status.isin(['Partly Delivered', 'Not Delivered']))
		.where((soi.qty - soi.delivered_qty) > 0)
		.where(soi.item_code.like('G%%'))
		.select(
			so.customer.as_('customer'),
			so.conditions.as_('so_remarks'),
			so.planning_remarks.as_('planning_remarks'),
			so.name.as_('sales_order'),
			soi.item_code.as_('item_code'),
			Sum(
				Case().when(Base(0, soi.actual_qty) -  	Base(0, soi.qty - soi.delivered_qty) > 0, 0)
				.else_(Base(0, soi.qty - soi.delivered_qty) - Base(0, soi.actual_qty))
			).as_('need_qty'),
			Sum(soi.qty - soi.delivered_qty).as_('pending_qty'),
			Sum(soi.stock_reserved_qty).as_('stock_reserved_qty'),
			soi.warehouse.as_('brand'),
			Sum(Base(0, soi.actual_qty)).as_('stock_qty'),
			so.delivery_status,
			so.delivery_status.as_('delivery_status')
		)
		.groupby(so.name)
	)	
	data = query.run(as_dict=True)
	return data

def get_so_items(filters):
	so = frappe.qb.DocType('Sales Order')
	soi = frappe.qb.DocType('Sales Order Item')
	query = (
		frappe.qb
		.from_(so)
		.left_join(soi).on(so.name == soi.parent)
		.where(so.status.notin(['Stopped', 'Closed']) & so.docstatus == 1)
		.where(soi.item_group == "Geyser Unit")
		.where(so.delivery_status.isin(['Partly Delivered', 'Not Delivered']))
		.where((soi.qty - soi.delivered_qty) > 0)
		.where(soi.item_code.like('G%%'))
		.select(
			soi.item_code.as_('item_code'),
			so.customer.as_('customer'),
			so.conditions.as_('so_remarks'),
			so.planning_remarks.as_('planning_remarks'),
			so.name.as_('sales_order'),
			soi.item_code.as_('item_code'),
			(
				Case().when(Base(0, soi.actual_qty) -  Base(0, soi.qty - soi.delivered_qty) > 0, 0)
				.else_(Base(0, soi.qty - soi.delivered_qty) - Base(0, soi.actual_qty))
			).as_('need_qty'),
			(soi.qty - soi.delivered_qty).as_('pending_qty'),
			(soi.stock_reserved_qty).as_('stock_reserved_qty'),
			soi.warehouse.as_('brand'),
			(Base(0, soi.actual_qty)).as_('stock_qty'),
			so.delivery_status,
			so.delivery_status.as_('delivery_status')
		)
	)	
	data = query.run(as_dict=True)
	return data

def get_data(filters=None):
	if filters.get('report_type') == 'Order and Shortage':
		sos = get_sales_order_data(filters)
	if filters.get('report_type') == 'Itemwise Order and Shortage':
		sos = get_so_items(filters)
	for so in sos:
		so['%'] = ((so['pending_qty'] - so['need_qty'])/ so['pending_qty'] )*100
		so['brand'] = so['brand'].replace(' - RAPL', '')
		so['stock_qty'] = so['stock_qty'] - so['stock_reserved_qty']
		if so['%'] >= 100:
			so['%'] = 100
	return sos


def get_columns(filters=None):
	builder = report_utils.ColumnBuilder()
	cols = None
	if filters.get('report_type') == 'Order and Shortage':
		cols = (builder
			.add_column("Customer", "Link", 300, "customer", options="Customer")
			.add_column("Sales Order", "Link", 150, "sales_order", options="Sales Order")
			.add_column("Pending Qty", "Int", 150, "pending_qty")
			.add_column("Stock Qty", "Int", 150, "stock_qty")
			.add_column("Remanin Qty", "Int", 150, "need_qty")
			.add_column("%", "Int", 150, "%", disable_total=True)
			.add_column("Brand", "Data", 200, "brand")
			.add_column("DS", "Data", 150, "delivery_status")
			.add_column("Planning Remarks", "HTML", 350, "planning_remarks")
			.add_column("Reserved", "Int", 80, "stock_reserved_qty")
			.build()
		)
	elif filters.get('report_type') == 'Itemwise Order and Shortage':
		cols = (builder
			.add_column("Customer", "Link", 300, "customer", options="Customer")
			.add_column("Geyser", "Link", 100, "item_code", options="Item")
			.add_column("Sales Order", "Link", 100, "sales_order", options="Sales Order")
			.add_column("Pending Qty", "Int", 100, "pending_qty")
			.add_column("Stock Qty", "Int", 100, "stock_qty")
			.add_column("Remanin Qty", "Int", 100, "need_qty")
			.add_column("%", "Int", 100, "%", disable_total=True)
			.add_column("Brand", "Data", 200, "brand")
			.add_column("Reserved", "Int", 80, "stock_reserved_qty")
			.add_column("DS", "Data", 100, "delivery_status")
			.add_column("Planning Remarks", "HTML", 100, "planning_remarks")
			.build()
		)
	return cols