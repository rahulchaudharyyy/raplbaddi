# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from raplbaddi.stock_rapl.report.pb_at_supplier.pb_at_supplier import accum_mapper, mapper, all_boxes, get_supplier_and_warehouse, remove_negative, get_supplierwise_po, warehouse_qty, date
from frappe.query_builder import DocType
from frappe.query_builder.functions import Concat, Sum, GroupConcat, Coalesce
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
        .where(so.docstatus == 1)
        .where(so.status.notin(['Stopped', 'Closed']))
        .where((soi.qty - soi.delivered_qty) > 0)
        .select(
            Sum(soi.qty - soi.delivered_qty).as_('so_qty'),
            soi.custom_box.as_('box'),
            GroupConcat(Concat('<a href="', url,'/app/sales-order/', so.name, '">', so.name, '</a>')).as_('so_name')
        )
        .groupby(soi.custom_box)
    )
    return remove_negative(['warehouse_qty'], so_query.run(as_dict=True))

def get_supplier_priority():
    psp = DocType('Paper Supplier Priority')
    pp_query = (
        frappe.qb
        .from_(psp)
        .select(
            psp.paper_name, psp.supplier, psp.priority, psp.parent
        )
    )
    print(accum_mapper(data=pp_query.run(as_dict=True), key='parent'))

def get_mr_data(supplier):
    mr = frappe.qb.DocType("Material Request")
    mr_item = frappe.qb.DocType("Material Request Item")
    query = (
        frappe.qb.from_(mr)
        .join(mr_item)
        .on(mr_item.parent == mr.name)
        .select(
            mr_item.item_code.as_("box"),
            (Sum(Coalesce(mr_item.qty, 0))).as_("qty")
        )
        .where(
            (mr.material_request_type == "Purchase")
            & (mr.docstatus == 1)
            & (mr.status != "Stopped")
            & (mr.per_received < 100)
            & (mr.supplier == supplier)
        )
    )

    query = query.groupby(mr_item.item_code).orderby(mr.transaction_date, mr.schedule_date)
    data = query.run(as_dict=True)
    return data

def join(filters=None):
    all_box = all_boxes()
    mr_jai_ambey = mapper(data=get_mr_data('Jai Ambey Industries'), key='box')
    mr_amit = mapper(data=get_mr_data("Amit Print 'N' Pack, Kishanpura, Baddi"), key='box')
    print(mr_amit)
    so = so_qty()
    rapl_warehouse_box = warehouse_qty(warehouse='Packing Boxes - Rapl')
    rapl_warehouse_box_mapping = {item['box']: item for item in rapl_warehouse_box}
    so_box_mapping = {item['box']: item for item in so}
    
    jai_ambey_supplier, jai_ambey_warehouse = 'Jai Ambey Industries', 'Jai Ambey Industries - RAPL'
    jai_ambey_warehouse_box = mapper(data=warehouse_qty(jai_ambey_warehouse), key='box')
    jai_ambey_warehouse_po_box = mapper(data=get_supplierwise_po(jai_ambey_supplier), key='box')
    
    amit_supplier, amit_warehouse = "Amit Print 'N' Pack, Kishanpura, Baddi", "Amit Print 'N' Pack - RAPL"
    amit_warehouse_box = mapper(data=warehouse_qty(amit_warehouse), key='box')
    amit_warehouse_po_box = mapper(data=get_supplierwise_po(amit_supplier), key='box')
    
    for box in all_box:
        box_name = box['box']
        
        if box_name in mr_amit:
            box['production_amit'] = mr_amit[box_name]['qty']
        else:
            box['production_amit'] = 0.0
        if box_name in mr_jai_ambey:
            box['production_jai_ambey'] = mr_jai_ambey[box_name]['qty']
        else:
            box['production_jai_ambey'] = 0.0
        
        if box_name in so_box_mapping:
            box['so_qty'] = so_box_mapping[box_name]['so_qty']
            box['so_name'] = so_box_mapping[box_name]['so_name']
        else:
            box['so_qty'] = 0.0
        
        if box_name in rapl_warehouse_box_mapping:
            box['stock_rapl'] = rapl_warehouse_box_mapping[box_name]['warehouse_qty']
            box['projected_rapl'] = rapl_warehouse_box_mapping[box_name]['projected_qty']
        else:
            box['stock_rapl'] = 0.0
            box['projected_rapl'] = 0.0

        if box_name in jai_ambey_warehouse_box:
            box['stock_jai_ambey'] = jai_ambey_warehouse_box[box_name]['warehouse_qty']
        else:
            box['stock_jai_ambey'] = 0.0

        if box_name in jai_ambey_warehouse_po_box:
            box['dispatch_jai_ambey'] = jai_ambey_warehouse_po_box[box_name]['box_qty']
            box['po_name_jai_ambey'] = jai_ambey_warehouse_po_box[box_name]['po_name']
        else:
            box['dispatch_jai_ambey'] = 0.0
        
        if box_name in amit_warehouse_box:
            box['stock_amit'] = amit_warehouse_box[box_name]['warehouse_qty']
        else:
            box['stock_amit'] = 0.0

        if box_name in amit_warehouse_po_box:
            box['dispatch_amit'] = amit_warehouse_po_box[box_name]['box_qty']
            box['po_name_amit'] = amit_warehouse_po_box[box_name]['po_name']
        else:
            box['dispatch_amit'] = 0.0

        if True:
            box['short_qty'] = (box['so_qty'] + box['msl']) - (box['stock_rapl'] + box['stock_jai_ambey'] + box['stock_amit'] + box['production_amit'] + box['production_jai_ambey'])
            if box['short_qty'] <= 0:
                box['short_qty'] = 0
            box['dispatch_need_to_complete_so'] = box['stock_rapl'] - box['so_qty'] + box['dispatch_jai_ambey'] + box['dispatch_amit']
            if box['dispatch_need_to_complete_so'] < 0:
                box['dispatch_need_to_complete_so'] = - box['dispatch_need_to_complete_so']
            else:
                box['dispatch_need_to_complete_so'] = 0
    
    all_box.sort(key=lambda x: x['short_qty'], reverse=True)
    return all_box

def columns(filters=None):
    cols = [{"label": "Item", "fieldtype": "Link", "width": 180, "options": "Item", "fieldname": 'box'},
            {"label": "JAI Stock", "fieldtype": "Int", "width": 60, "fieldname": "stock_jai_ambey"},
            {"label": "Amit Stock", "fieldtype": "Int", "width": 60, "fieldname": "stock_amit"},
            {"label": "Rapl Stock", "fieldtype": "Int", "width": 60, "fieldname": "stock_rapl"},
            {"label": "Dispatch Need SO", "fieldtype": "Int", "width": 100, "fieldname": 'dispatch_need_to_complete_so'},
            {"label": "Σ Projected", "fieldtype": "Int", "width": 60, "fieldname": "projected_rapl"},
            {"label": "SO", "fieldtype": "Int", "width": 60, "fieldname": "so_qty"},
            {"label": "Production JAI", "fieldtype": "Int", "width": 100, "fieldname": 'production_jai_ambey'},
            {"label": "Dispatch JAI", "fieldtype": "Int", "width": 100, "fieldname": 'dispatch_jai_ambey'},
            {"label": "Production Amit", "fieldtype": "Int", "width": 100, "fieldname": 'production_amit'},
            {"label": "Dispatch Amit", "fieldtype": "Int", "width": 100, "fieldname": 'dispatch_amit'},
            {"label": "MSL", "fieldtype": "Int", "width": 100, "fieldname": 'msl', 'disable_total': True},
            {"label": "Shortage", "fieldtype": "Int", "width": 100, "fieldname": 'short_qty'},
            {"label": "SOs", "fieldtype": "HTML", "width": 100, "fieldname": 'so_name'},
            {"label": "POs Amit", "fieldtype": "HTML", "width": 100, "fieldname": 'po_name_amit'},
            {"label": "POs JAI", "fieldtype": "HTML", "width": 100, "fieldname": 'po_name_jai_ambey'}
    ]
    return cols
