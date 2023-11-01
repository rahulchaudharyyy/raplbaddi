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

def get_stock_balance(filters):
	bin = frappe.qb.DocType('Bin')
	query = (
		frappe.qb
		.from_(bin)
		.select(bin.item_code, bin.warehouse, bin.actual_qty)
		.where(bin.item_code.like('G%%'))
	)
	return query.run(as_dict=True)

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
			Case().when(so.submission_date, so.submission_date).else_(so.transaction_date).as_('date'),
			soi.item_code.as_('item_code'),
			so.customer.as_('customer'),
			so.conditions.as_('so_remarks'),
			so.planning_remarks.as_('planning_remarks'),
			so.name.as_('sales_order'),
			soi.item_code.as_('item_code'),
			Base(0, soi.qty - soi.delivered_qty).as_('pending_qty'),
			(soi.stock_reserved_qty).as_('stock_reserved_qty'),
			soi.warehouse.as_('brand'),
			so.delivery_status,
			so.delivery_status.as_('delivery_status')
		)
	)	
	data = query.run(as_dict=True)
	return data

def get_data(filters=None):
	bins = get_stock_balance(filters)
	sos = get_so_items(filters)
	total_short_qty = 0 
	total_pending_qty = 0 

	for so in sos:
		so['brand'] = so['brand'].replace(' - RAPL', '')
		for bin in bins:
			item_code = bin.get('item_code')
			actual_qty = bin.get('actual_qty')
			brand = bin.get('warehouse').replace(' - RAPL', '')
			if item_code == so['item_code'] and brand == so['brand']:
				so['short_qty'] = (min(0, actual_qty - so['pending_qty']))
				total_short_qty += so['short_qty']
		total_pending_qty += so['pending_qty']

		percentage = ((actual_qty - so['pending_qty']) / so['pending_qty']) * 100
		so['%'] = max(0, min(100, percentage))
	if filters.get('report_type') == 'Order and Shortage':
		percentage = total_short_qty / total_pending_qty * 100
		so['%'] = max(0, min(100, percentage))
	return sos




def get_columns(filters=None):
	builder = report_utils.ColumnBuilder()
	cols = None
	if filters.get('report_type') == 'Order and Shortage':
		cols = (builder
			.add_column("Date", "Date", 100, "date")
			.add_column("Planning", "HTML", 100, "planning_remarks")
			.add_column("Item", "Link", 100, "item_code", options="Item")
			.add_column("Sales Order", "Link", 100, "sales_order", options="Sales Order")
			.add_column("Customer", "Link", 300, "customer", options="Customer")
			.add_column("Pending Qty", "Int", 120, "pending_qty")
			.add_column("%", "Int", 40, "%", disable_total=True)
			.add_column("Brand", "Data", 100, "brand")
   			.add_column("SO Remark", "HTML", 130, "so_remarks")
			.build()
		)
	elif filters.get('report_type') == 'Itemwise Order and Shortage':
		cols = (builder
			.add_column("Date", "Date", 100, "date")
			.add_column("Planning", "HTML", 100, "planning_remarks")
			.add_column("Sales Order", "Link", 100, "sales_order", options="Sales Order")
			.add_column("Customer", "Link", 300, "customer", options="Customer")
			.add_column("Pending Qty", "Int", 120, "pending_qty")
			.add_column("Stock Qty", "Int", 100, "actual_qty")
			.add_column("Remanin Qty", "Int", 120, "need_qty")
			.add_column("%", "Int", 40, "%", disable_total=True)
			.add_column("Brand", "Data", 100, "brand")
   			.add_column("SO Remark", "HTML", 130, "so_remarks")
			.build()
		)
	return cols