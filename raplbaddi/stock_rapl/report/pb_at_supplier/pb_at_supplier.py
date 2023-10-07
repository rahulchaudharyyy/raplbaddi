# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count, Sum
from pypika.terms import Case, Not, Field, Order
from frappe.query_builder import AliasedQuery
from frappe.utils import getdate

date = getdate('1-1-1')

def execute(filters=None):
    return columns(filters), join()

def get_supplier_and_warehouse() -> str:
    user = frappe.session.user
    if user == 'production.jaiambey2024@gmail.com':
        supplier = 'Jai Ambey Industries'
        warehouse = 'Jai Ambey Industries - Rapl'
    if user == 'ppic@amitprintpack.com':
        supplier = "Amit Print 'N' Pack, Kishanpura, Baddi"
        warehouse = "Amit Print 'N' Pack - RAPL"
    else:
        warehouse = ''
    supplier = "Amit Print 'N' Pack, Kishanpura, Baddi"
    warehouse = "Amit Print 'N' Pack - RAPL"
    return supplier, warehouse

def all_boxes() -> dict:
    items = DocType('Item')
    box_query = (
        frappe.qb
        .from_(items)
        .where(items.item_group == "Packing Boxes").where(items.disabled == 0)
        .select(items.name.as_('box'))
    )
    return box_query.run(as_dict=True)

def get_supplierwise_po(supplier: str) -> dict:
    poi = DocType('Purchase Order Item')
    po = DocType('Purchase Order')
    jai_ambey_po_query = (
        frappe.qb
        .from_(poi)
        .left_join(po)
        .on(po.name == poi.parent)
        .where(po.supplier == supplier)
        .where(po.docstatus == 1)
        .select(
            Sum(poi.qty - poi.received_qty).as_('box_qty'),
            poi.item_code.as_('box'),
            Sum(poi.planned_dispatch_qty - poi.received_qty).as_('planned_qty'),
            po.transaction_date.as_('po_date') 
        )
        .groupby(poi.item_code)
    )
    return jai_ambey_po_query.run(as_dict=True)

def join():
    all_box = all_boxes()
    supplier, warehouse = get_supplier_and_warehouse()
    warehouse_box = warehouse_qty(warehouse)
    po_box = remove_negative(['box_qty', 'planned_qty'], get_supplierwise_po(supplier))

    warehouse_box_mapping = {item['box']: item for item in warehouse_box}
    po_box_mapping = {item['box']: item for item in po_box}

    filtered_box = []

    for box in all_box:
        box_name = box['box']

        if box_name in warehouse_box_mapping:
            box['warehouse_qty'] = warehouse_box_mapping[box_name]['warehouse_qty']
        else:
            box['warehouse_qty'] = 0.0

        if box_name in po_box_mapping:
            box['box_qty'] = po_box_mapping[box_name]['box_qty']
            box['planned_qty'] = po_box_mapping[box_name]['planned_qty']
            box['po_date'] = po_box_mapping[box_name]['po_date']
        else:
            box['box_qty'] = 0.0
            box['planned_qty'] = 0.0
            box['po_date'] = date

        if box['warehouse_qty'] != 0.0 or box['box_qty'] != 0.0 or box['planned_qty'] != 0.0:
            filtered_box.append(box)

    filtered_box.sort(key=lambda x: x['po_date'], reverse=True)

    return filtered_box

def remove_negative(keys: list, data: list[dict]) -> dict:
    for key in keys:
        for d in data:
            if d.get(key, 0) < 0:
                d[key] = 0
    return data

def warehouse_qty(warehouse: str) -> dict:
    item = DocType('Item')
    bin = DocType('Bin')
    qty_query = (
        frappe.qb
        .from_(item)
        .left_join(bin)
        .on(item.name == bin.item_code)
        .where(bin.warehouse == warehouse)
        .select(
            bin.actual_qty.as_('warehouse_qty'),
            item.name.as_('box'),
        )
    )
    return remove_negative(['warehouse_qty'], qty_query.run(as_dict=True))

def columns(filters=None):
   cols = [{"label": "item", "fieldtype": "Link", "width": 180, "options": "Item", "fieldname": 'box'},
        {"label": "Date", "fieldtype": "Date", "width": 120, "fieldname": "po_date"},
        {"label": "Stock", "fieldtype": "Int", "width": 60, "fieldname": "warehouse_qty"},
        {"label": "Production", "fieldtype": "Int", "width": 100, "fieldname": 'box_qty'},
        {"label": "Dispatch", "fieldtype": "Int", "width": 100, "fieldname": 'planned_qty'},
    ]
   return cols