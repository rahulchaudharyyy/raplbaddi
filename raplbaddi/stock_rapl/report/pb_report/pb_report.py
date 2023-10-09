# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from raplbaddi.stock_rapl.report.pb_at_supplier.pb_at_supplier import all_boxes, get_supplier_and_warehouse, remove_negative, get_supplierwise_po, warehouse_qty, date
from frappe.query_builder import DocType
from frappe.query_builder.functions import Concat, Sum, GroupConcat
from frappe.utils import get_url

def execute(filters=None):
    return columns(), join()

def so_qty() -> dict:
    so = DocType('Sales Order')
    soi = DocType('Sales Order Item')
    url = get_url()
    so_query = (
        frappe.qb
        .from_(so)
        .left_join(soi)
        .on(so.name == soi.parent)
        .select(
            Sum(soi.qty - soi.delivered_qty).as_('so_qty'),
            soi.custom_box.as_('box'),
            GroupConcat(Concat('<a href="', url,'/app/sales-order/', so.name, '">', so.name, '</a>')).as_('so_name')
        )
        .groupby(soi.custom_box)
    )
    return remove_negative(['warehouse_qty'], so_query.run(as_dict=True))

def join(filters=None):
    all_box = all_boxes()
    so = so_qty()
    rapl_warehouse_box = warehouse_qty(warehouse='Packing Boxes - Rapl')
    rapl_warehouse_box_mapping = {item['box']: item for item in rapl_warehouse_box}
    so_box_mapping = {item['box']: item for item in so}
    
    jai_ambey_warehouse_box = warehouse_qty(warehouse='Jai Ambey Industries - Rapl')
    jai_ambey_po_box = remove_negative(['box_qty', 'planned_qty'], get_supplierwise_po(supplier='Jai Ambey Industries'))
    jai_ambey_warehouse_box_mapping = {item['box']: item for item in jai_ambey_warehouse_box}
    jai_ambey_po_box_mapping = {item['box']: item for item in jai_ambey_po_box}
    
    amit_warehouse_box = warehouse_qty(warehouse="Amit Print 'N' Pack - RAPL")
    amit_po_box = remove_negative(['box_qty', 'planned_qty'], get_supplierwise_po(supplier="Amit Print 'N' Pack"))
    amit_warehouse_box_mapping = {item['box']: item for item in amit_warehouse_box}
    amit_po_box_mapping = {item['box']: item for item in amit_po_box}

    filtered_box = []

    for box in all_box:
        box_name = box['box']
        
        if box_name in so_box_mapping:
            box['so_qty'] = so_box_mapping[box_name]['so_qty']
            box['so_name'] = so_box_mapping[box_name]['so_name']
            print(box['so_name'])
        else:
            box['so_qty'] = 0.0
        
        if box_name in rapl_warehouse_box_mapping:
            box['rapl_qty'] = rapl_warehouse_box_mapping[box_name]['warehouse_qty']
        else:
            box['rapl_qty'] = 0.0

        if box_name in jai_ambey_warehouse_box_mapping:
            box['jai_ambey_warehouse_qty'] = jai_ambey_warehouse_box_mapping[box_name]['warehouse_qty']
        else:
            box['jai_ambey_warehouse_qty'] = 0.0

        if box_name in jai_ambey_po_box_mapping:
            box['jai_ambey_box_qty'] = jai_ambey_po_box_mapping[box_name]['box_qty']
            box['jai_ambey_planned_qty'] = jai_ambey_po_box_mapping[box_name]['planned_qty']
            box['jai_ambey_po'] = jai_ambey_po_box_mapping[box_name]['po_name']
        else:
            box['jai_ambey_box_qty'] = 0.0
            box['jai_ambey_planned_qty'] = 0.0
            
        
        if box_name in amit_warehouse_box_mapping:
            box['amit_warehouse_qty'] = amit_warehouse_box_mapping[box_name]['warehouse_qty']
        else:
            box['amit_warehouse_qty'] = 0.0

        if box_name in amit_po_box_mapping:
            box['amit_box_qty'] = amit_po_box_mapping[box_name]['box_qty']
            box['amit_planned_qty'] = amit_po_box_mapping[box_name]['planned_qty']
            box['amit_po'] = jai_ambey_po_box_mapping[box_name]['po_name']
            if box['amit_planned_qty'] < 
        else:
            box['amit_box_qty'] = 0.0
            box['amit_planned_qty'] = 0.0

        if True:
            box['short_qty'] = (box['so_qty'] + box['msl']) - (box['rapl_qty'] + box['jai_ambey_warehouse_qty'] + box['amit_warehouse_qty'] + box['jai_ambey_box_qty'] + box['amit_box_qty'])
            if box['short_qty'] <= 0:
                box['short_qty'] = 0
    
    return all_box

def columns(filters=None):
    cols = [{"label": "Item", "fieldtype": "Link", "width": 180, "options": "Item", "fieldname": 'box'},
            {"label": "JAI Stock", "fieldtype": "Int", "width": 60, "fieldname": "jai_ambey_warehouse_qty"},
            {"label": "Amit Stock", "fieldtype": "Int", "width": 60, "fieldname": "amit_warehouse_qty"},
            {"label": "Rapl Stock", "fieldtype": "Int", "width": 60, "fieldname": "rapl_qty"},
            {"label": "SO", "fieldtype": "Int", "width": 60, "fieldname": "so_qty"},
            {"label": "Production JAI", "fieldtype": "Int", "width": 100, "fieldname": 'jai_ambey_box_qty'},
            {"label": "Dispatch JAI", "fieldtype": "Int", "width": 100, "fieldname": 'jai_ambey_planned_qty'},
            {"label": "Production Amit", "fieldtype": "Int", "width": 100, "fieldname": 'amit_box_qty'},
            {"label": "Dispatch Amit", "fieldtype": "Int", "width": 100, "fieldname": 'amit_planned_qty'},
            {"label": "MSL", "fieldtype": "Int", "width": 100, "fieldname": 'msl', 'disable_total': True},
            {"label": "Shortage", "fieldtype": "Int", "width": 100, "fieldname": 'short_qty'},
            {"label": "SOs", "fieldtype": "HTML", "width": 100, "fieldname": 'so_name'},
            {"label": "POs Amit", "fieldtype": "HTML", "width": 100, "fieldname": 'amit_po'},
            {"label": "POs JAI", "fieldtype": "HTML", "width": 100, "fieldname": 'jai_ambey_po'}
    ]
    return cols
