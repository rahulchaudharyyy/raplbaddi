# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from frappe import _
import frappe
from frappe.query_builder.functions import Sum
from raplbaddi.utils import report_utils
from raplbaddi.salesrapl.report.geyser_production_planning import sales_order_data
from erpnext.stock.doctype.stock_reservation_entry import stock_reservation_entry

def execute(filters=None):
	columns, datas = [], []
	columns = get_columns(filters)
	if filters.get('report_type') == "Order and Shortage":
		get_available_qty_to_reserve()
		datas = so()
	elif filters.get('report_type') == "Itemwise Order and Shortage":
		datas = soi()
	return columns, datas

def get_available_qty_to_reserve():
	bins = sales_order_data.get_bin_stock()
	sres = get_sre()
	for bin in bins:
		item = bin['item_code']
		warehouse = bin['warehouse']
		reserved_qty = 0
		for sre in sres:
			if sre.get('item_code') == item and sre.get('warehouse') == warehouse:
				reserved_qty += sre.get('reserved_qty')
			bin['available_qty_to_reserve'] = bin['actual_qty'] - reserved_qty
			bin['reserved'] = 1 if reserved_qty > 0 else 0
			bin['reserved_qty'] = reserved_qty
	return bins

def get_sre():
	sre = frappe.qb.DocType("Stock Reservation Entry")
	query = (
		frappe.qb.from_(sre)
		.select((sre.reserved_qty - sre.delivered_qty).as_('reserved_qty'), sre.warehouse, sre.item_code)
		.where(
			(sre.docstatus == 1)
			& (sre.reserved_qty >= sre.delivered_qty)
			& (sre.status.notin(["Delivered", "Cancelled"]))
		)
	)
	ret = query.run(as_dict=True)
	return ret


def soi():
	data = sales_order_data.get_so_items()
	bins = get_available_qty_to_reserve()
	boxes = sales_order_data.get_box_qty()
	for soi in data:
		soi['brand'] = soi['brand'].replace('- RAPL', '')
		for bin_val in bins:
			if bin_val['item_code'] == soi['item_code'] and bin_val['warehouse'].replace('- RAPL', '') == soi['brand']:
				short = 0
				if bin_val['available_qty_to_reserve'] - soi['pending_qty'] > 0:
					short = 0
				else:
					short = soi['pending_qty'] - bin_val['available_qty_to_reserve']
				soi['%'] = 100 - (short / soi['pending_qty']) * 100
				soi['actual_qty'] = bin_val['actual_qty']
				soi['short_qty'] = short
				soi['available_qty_to_reserve'] = bin_val['available_qty_to_reserve']
				soi['reserved_qty'] = bin_val['reserved_qty']
				soi['reserved'] = bin_val['reserved']
		for box in boxes:
			if box.get('box') == soi['box']:
				soi['box_stock_qty'] = box['warehouse_qty']
	data.sort(reverse=True, key= lambda entry: entry['%'])
	return data

def so():
	data = []
	so = report_utils.accum_mapper(data=(sales_order_data.get_so_items()), key='sales_order')
	bin = get_available_qty_to_reserve()
	for so, so_val in so.items():
		entry = {}
		entry['sales_order'] = so
		entry['pending_qty'] = 0
		entry['so_shortage'] = 0
		entry['so_shortage'] = 0
		items, brands = set(), set()
		for soi in so_val:
			entry['pending_qty'] += soi['pending_qty']
			entry['status'] = soi['status']
			entry['planning_remarks'] = soi['planning_remarks']
			entry['so_remarks'] = soi['so_remarks']
			entry['date'] = soi['date']
			entry['customer'] = soi['customer']
			soi_shortage = 0
			items.add(soi['item_code'])
			brands.add(soi['brand'].replace(' - RAPL', ''))
			for bin_val in bin:
				if bin_val['item_code'] == soi['item_code'] and bin_val['warehouse'] == soi['brand']:
					short = 0
					if bin_val.get('available_qty_to_reserve', 0) - soi['pending_qty'] > 0:
						short = 0
					else:
						short = soi['pending_qty'] - bin_val.get('available_qty_to_reserve')
					soi_shortage += short
			entry['so_shortage'] += soi_shortage
		entry['items'] = ', '.join(items)
		entry['brands'] = ', '.join(brands)
		entry['%'] = 100 - (entry['so_shortage'] / entry['pending_qty']) * 100
		data.append(entry)
		data.sort(reverse=True, key= lambda entry: entry['%'])
	return data

def get_columns(filters=None):
	cols = None
	if filters.get('report_type') == 'Itemwise Order and Shortage':
		builder = report_utils.ColumnBuilder()
		cols = (builder
			.add_column("Date", "Date", 100, "date")
			.add_column("Planning", "HTML", 100, "planning_remarks")
			.add_column("Item", "Link", 100, "item_code", options="Item")
			.add_column("Box", "Link", 100, "box", options="Item")
			.add_column("Box Qty", "Int", 120, "box_stock_qty")
			.add_column("Sales Order", "Link", 100, "sales_order", options="Sales Order")
			.add_column("Customer", "Link", 300, "customer", options="Customer")
			.add_column("Order Qty", "Int", 120, "pending_qty")
			.add_column("Actual Qty", "Int", 120, "actual_qty")
			.add_column("Reserved", "Int", 120, "reserved")
			.add_column("Reserved Qty", "Int", 120, "reserved_qty", disable_total=True)
			.add_column("After reserved Qty", "Int", 120, "available_qty_to_reserve")
			.add_column("Short Qty", "Int", 120, "short_qty")
			.add_column("%", "Int", 40, "%", disable_total=True)
			.add_column("Brand", "Data", 100, "brand")
   			.add_column("SO Remark", "HTML", 130, "so_remarks")
			.build()
		)
	if filters.get('report_type') == 'Order and Shortage':
		builder = report_utils.ColumnBuilder()
		cols = (builder
			.add_column("Date", "Date", 100, "date")
			.add_column("Items", "Data", 100, "items")
			.add_column("Planning", "HTML", 100, "planning_remarks")
			.add_column("Status", "Data", 100, "status")
			.add_column("Sales Order", "Link", 100, "sales_order", options="Sales Order")
			.add_column("Customer", "Link", 300, "customer", options="Customer")
			.add_column("Order Qty", "Int", 120, "pending_qty")
			.add_column("Shortage Qty", "Int", 100, "so_shortage")
			.add_column("% Available", "Int", 100, "%", disable_total=True)
			.add_column("Brand", "Data", 100, "brands")
			.add_column("SO Remark", "HTML", 130, "so_remarks")
			.build()
		)
	return cols