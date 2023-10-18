# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from raplbaddi.stock_rapl.report.pb_at_supplier.pb_at_supplier import accum_mapper, mapper, all_boxes, get_supplier_and_warehouse, remove_negative, get_supplierwise_po, warehouse_qty, date
from frappe.query_builder import DocType
from frappe.query_builder.functions import Concat, Sum, GroupConcat, Coalesce
from frappe.utils import get_url
from raplbaddi.utils import report_utils
from raplbaddi.stock_rapl.report.pb_report import box_data

def execute(filters=None):
    return columns(), join()

def get_box_data(box_name, mr_dict, column_name):
    return mr_dict.get(box_name, {}).get(column_name, 0.0)

def get_warehouse_data(warehouse_name):
    warehouse_data = warehouse_qty(warehouse=warehouse_name)
    return {item['box']: item for item in warehouse_data}

def join(filters=None):
    all_box = all_boxes()
    mr_amit = report_utils.get_mapped_data(data=box_data.get_box_order_for_production("Amit Print 'N' Pack, Kishanpura, Baddi"), key='box')
    mr_jai_ambey = report_utils.get_mapped_dataget_mapped_data(data=box_data.get_box_order_for_production('Jai Ambey Industries'), key='box')
    so_mapping = report_utils.get_mapped_dataget_mapped_data(data=box_data.get_box_requirement_from_so(), key='box')
    rapl_warehouse_mapping = get_warehouse_data('Packing Boxes - Rapl')
    jai_ambey_warehouse_mapping = get_warehouse_data('Jai Ambey Industries - RAPL')
    amit_warehouse_mapping = get_warehouse_data("Amit Print 'N' Pack - RAPL")

    jai_ambey_supplier = 'Jai Ambey Industries'
    amit_supplier = "Amit Print 'N' Pack, Kishanpura, Baddi"

    jai_ambey_warehouse_po_box = report_utils.get_mapped_dataget_mapped_data(data=get_supplierwise_po(jai_ambey_supplier), key='box')
    amit_warehouse_po_box = report_utils.get_mapped_data(data=get_supplierwise_po(amit_supplier), key='box')

    for box in all_box:
        box_name = box['box']
        box['production_amit'] = get_box_data(box_name, mr_amit, 'qty')
        box['production_jai_ambey'] = get_box_data(box_name, mr_jai_ambey, 'qty')

        box['so_qty'] = so_mapping.get(box_name, {'so_qty': 0.0})['so_qty']
        box['so_name'] = so_mapping.get(box_name, {'so_name': ''})['so_name']

        warehouse_item = rapl_warehouse_mapping.get(box_name, {'warehouse_qty': 0.0, 'projected_qty': 0.0})
        box['stock_rapl'] = warehouse_item['warehouse_qty']
        box['projected_rapl'] = warehouse_item['projected_qty']

        warehouse_item = jai_ambey_warehouse_mapping.get(box_name, {'warehouse_qty': 0.0})
        box['stock_jai_ambey'] = warehouse_item['warehouse_qty']

        warehouse_item = amit_warehouse_mapping.get(box_name, {'warehouse_qty': 0.0})
        box['stock_amit'] = warehouse_item['warehouse_qty']

        box['dispatch_jai_ambey'] = jai_ambey_warehouse_po_box.get(box_name, {'box_qty': 0.0})['box_qty']
        box['po_name_jai_ambey'] = jai_ambey_warehouse_po_box.get(box_name, {'po_name': ''})['po_name']

        box['dispatch_amit'] = amit_warehouse_po_box.get(box_name, {'box_qty': 0.0})['box_qty']
        box['po_name_amit'] = amit_warehouse_po_box.get(box_name, {'po_name': ''})['po_name']

    for box in all_box:
        box['short_qty'] = max(0, (box['so_qty'] + box['msl']) - (box['stock_rapl'] + box['stock_jai_ambey'] + box['stock_amit'] + box['production_amit'] + box['production_jai_ambey']))
        box['dispatch_need_to_complete_so'] = max(0, box['stock_rapl'] - box['so_qty'] + box['dispatch_jai_ambey'] + box['dispatch_amit'])

    all_box.sort(key=lambda x: x['short_qty'], reverse=True)
    return all_box

def columns(filters=None):
    builder = report_utils.ColumnBuilder()
    cols = (builder 
        .add_column("Item", "Link", 180, "box", options="Item") 
        .add_column("JAI Stock", "Int", 60, "stock_jai_ambey") 
        .add_column("Amit Stock", "Int", 60, "stock_amit") 
        .add_column("Rapl Stock", "Int", 60, "stock_rapl") 
        .add_column("Dispatch Need SO", "Int", 100, "dispatch_need_to_complete_so") 
        .add_column("Σ Projected", "Int", 60, "projected_rapl") 
        .add_column("SO", "Int", 60, "so_qty") 
        .add_column("Production JAI", "Int", 100, "production_jai_ambey") 
        .add_column("Dispatch JAI", "Int", 100, "dispatch_jai_ambey") 
        .add_column("Production Amit", "Int", 100, "production_amit") 
        .add_column("Dispatch Amit", "Int", 100, "dispatch_amit") 
        .add_column("MSL", "Int", 100, "msl", disable_total=True) 
        .add_column("Shortage", "Int", 100, "short_qty") 
        .add_column("SOs", "HTML", 100, "so_name") 
        .add_column("POs Amit", "HTML", 100, "po_name_amit") 
        .add_column("POs JAI", "HTML", 100, "po_name_jai_ambey") 
        .build()
    )
    return cols