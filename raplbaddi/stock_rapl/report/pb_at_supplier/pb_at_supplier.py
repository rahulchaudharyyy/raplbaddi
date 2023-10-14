# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count, Sum
from pypika.terms import Case, Not, Field, Order
from frappe.query_builder import AliasedQuery
from frappe.utils import getdate
from raplbaddi.datarapl.doctype.report_full_access_users.report_full_access_users import get_wildcard_users
from frappe.query_builder.functions import Concat, Sum, GroupConcat
from frappe.utils import get_url

date = getdate('1-1-1')

def execute(filters=None):
    return columns(filters), join(filters)

def get_supplier_and_warehouse(filters=None, s='', w='') -> str:
    user = frappe.session.user
    supplier = s
    warehouse = w
    if user == 'production.jaiambey2024@gmail.com':
        supplier = 'Jai Ambey Industries'
        warehouse = 'Jai Ambey Industries - RAPL'
    elif user in ['ppic@amitprintpack.com', 'appdispatch01@gmail.com']:
        supplier = "Amit Print 'N' Pack, Kishanpura, Baddi"
        warehouse = "Amit Print 'N' Pack - RAPL"
    elif user in get_wildcard_users() and filters.get('supplier'):
        if filters.get('supplier') == 'Jai Ambey Industries':
            supplier = 'Jai Ambey Industries'
            warehouse = 'Jai Ambey Industries - RAPL'
        elif filters.get('supplier') == "Amit Print 'N' Pack, Kishanpura, Baddi":
            supplier = "Amit Print 'N' Pack, Kishanpura, Baddi"
            warehouse = "Amit Print 'N' Pack - RAPL"
    print(supplier, warehouse)
    return supplier, warehouse


def all_boxes() -> dict:
    items = DocType('Item')
    supplier_priority = DocType('Supplier Priority')
    box_query = (
        frappe.qb
        .from_(items)
        .where(items.item_group == "Packing Boxes").where(items.disabled == 0)
        .select(items.name.as_('box'), items.safety_stock.as_('msl'))
    )
    return box_query.run(as_dict=True)


def get_supplierwise_po(supplier: str) -> dict:
    poi = DocType('Purchase Order Item')
    po = DocType('Purchase Order')
    url = get_url()
    query = (
        frappe.qb
        .from_(poi)
        .left_join(po)
        .on(po.name == poi.parent)
        .where(po.supplier == supplier)
        .where(po.docstatus == 1)
        .where(po.status != 'Closed')
        .select(
            Sum(Case()
                .when(
                    (poi.qty - poi.received_qty) < 0, (poi.qty - poi.received_qty) - (poi.qty - poi.received_qty))
                .else_((poi.qty - poi.received_qty))
                ).as_('box_qty'),
            poi.item_code.as_('box'),
            Sum(Case()
                .when(
                    (poi.planned_dispatch_qty - poi.received_qty) < 0, (poi.planned_dispatch_qty - poi.received_qty) - (poi.planned_dispatch_qty - poi.received_qty))
                .else_((poi.planned_dispatch_qty - poi.received_qty))
                ).as_('planned_qty'),
            (Case()
                .when(
                    Sum(poi.planned_dispatch_qty - poi.received_qty) < 0, Sum(poi.received_qty - poi.planned_dispatch_qty))
                .else_(0)
                ).as_('over_dispatch'),
            po.transaction_date.as_('po_date'),
            GroupConcat(Concat('<a href="', url,'/app/purchase-order/', po.name, '">', po.name, '</a>')).as_('po_name'),
            Sum(poi.received_qty).as_('received_qty')
        )
        .groupby(poi.item_code)
    )
    return query.run(as_dict=True)

def mapper(data: list) -> dict:
    return {item['box']: item for item in data}

def join(filters=None):
    all_box = all_boxes()
    supplier, warehouse = get_supplier_and_warehouse(filters=filters)
    warehouse_box = mapper(warehouse_qty(warehouse))
    po_box = mapper(get_supplierwise_po(supplier))


    filtered_box = []

    for box in all_box:
        box_name = box['box']

        if box_name in warehouse_box:
            box['warehouse_qty'] = warehouse_box[box_name]['warehouse_qty']
        else:
            box['warehouse_qty'] = 0.0

        if box_name in po_box:
            box['box_qty'] = po_box[box_name]['box_qty']
            box['planned_qty'] = po_box[box_name]['planned_qty']
            box['over_dispatch'] = po_box[box_name]['over_dispatch']
            box['po_name'] = po_box[box_name]['po_name']
            box['po_date'] = po_box[box_name]['po_date']
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
            bin.projected_qty.as_('projected_qty')
        )
    )
    return remove_negative(['warehouse_qty'], qty_query.run(as_dict=True))

def columns(filters=None):
   cols = [{"label": "item", "fieldtype": "Link", "width": 180, "options": "Item", "fieldname": 'box'},
        {"label": "Date", "fieldtype": "Date", "width": 120, "fieldname": "po_date"},
        {"label": "Stock", "fieldtype": "Int", "width": 60, "fieldname": "warehouse_qty"},
        {"label": "Production Order", "fieldtype": "Int", "width": 100, "fieldname": 'box_qty'},
        {"label": "Dispatch Order", "fieldtype": "Int", "width": 100, "fieldname": 'planned_qty'},
        {"label": "Over Dispatch", "fieldtype": "Int", "width": 100, "fieldname": 'over_dispatch'},
        {"label": "PO", "fieldtype": "Html", "width": 100, "fieldname": 'po_name'}
    ]
   return cols