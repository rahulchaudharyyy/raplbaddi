# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Concat, Sum, GroupConcat, Coalesce
from frappe.utils import get_url
from raplbaddi.utils import report_utils
from raplbaddi.stock_rapl.report.pb_report.box_data import BoxRequirements

box_data = BoxRequirements()

def execute(filters=None):
    return columns(filters), join(filters)

def get_box_data(box_name, mr_dict, column_name):
    return mr_dict.get(box_name, {}).get(column_name, 0.0)

def get_warehouse_data(warehouse_name):
    warehouse_data = box_data.warehouse_qty(warehouse=warehouse_name)
    return {item['box']: item for item in warehouse_data}

class BoxProductionSort(report_utils.SortStrategy):
    def sort(self, data):
        return sorted(data, key=lambda x: x['short_qty'], reverse=True)

class BoxDispatchSort(report_utils.SortStrategy):
    def sort(self, data):
        return sorted(data, key=lambda x: x['dispatch_need_to_complete_so'], reverse=True)

class DeadStockSort(report_utils.SortStrategy):
    def sort(self, data):
        return sorted([item for item in data if item['dead_inventory'] > 0 and item['total_stock'] > 0], key=lambda x: x['total_stock'], reverse=True)

class UrgentDispatchSort(report_utils.SortStrategy):
    def sort(self, data):
        return sorted([item for item in data if item['urgent_dispatch'] > 0], key=lambda x: x['urgent_dispatch'], reverse=True)

class BoxStockSort(report_utils.SortStrategy):
    def sort(self, data):
        return sorted([item for item in data if item['stock_rapl'] > 0], key=lambda x: x['stock_rapl'], reverse=True)

class SortStrategyFactory:
    @staticmethod
    def get_strategy(report_type):
        strategies = {
            'Box Production': BoxProductionSort(),
            'Box Dispatch': BoxDispatchSort(),
            'Dead Stock': DeadStockSort(),
            'Urgent Dispatch': UrgentDispatchSort(),
            'Box Stock': BoxStockSort()
        }
        return strategies.get(report_type)

class Supplier:
    def __init__(self, name):
        self.name = name
        self.warehouse = get_warehouse_data(f"{name} - RAPL")
        self.mr = report_utils.get_mapped_data(data=box_data.get_box_order_for_production(self.name), key='box')
        self.po = report_utils.get_mapped_data(data=box_data.get_supplierwise_po(self.name), key='box')
        self.priority = report_utils.get_mapped_data(data=box_data.get_paper_supplier_priority(self.name), key='box')
    def get_supplier_data(self):
        return self.warehouse, self.mr, self.po, self.priority


def join(filters=None):
    all_box = box_data.all_boxes('Packing Boxes', 'box')
    all_paper = box_data.all_boxes('Packing Paper', 'paper')
    so = report_utils.get_mapped_data(data=box_data.get_box_requirement_from_so(), key='box')
    rapl_warehouse = get_warehouse_data('Packing Boxes - Rapl')


    warehouse_jai, mr_jai, po_jai, priority_jai = Supplier(name='Jai Ambey Industries').get_supplier_data()
    warehouse_amit, mr_amit, po_amit, priority_amit = Supplier(name="Amit Print 'N' Pack").get_supplier_data()
    warehouse_rana, mr_rana, po_rana, priority_rana = Supplier(name="Rana, Packing Box").get_supplier_data()

    for box in all_box:
        box_name = box.get('box', '-')

        box['so_qty'] = so.get(box_name, {'so_qty': 0.0})['so_qty']
        box['so_name'] = so.get(box_name, {'so_name': ''})['so_name']
                    
        box_particular = box.get('box_particular', '')
        paper_name = box.get('paper_name', '')
        paper_name = f'PP {box_particular} {paper_name}'
        
        warehouse_item = rapl_warehouse.get(box_name, {'warehouse_qty': 0.0, 'projected_qty': 0.0})
        box['stock_rapl'] = warehouse_item['warehouse_qty']
        box['projected_rapl'] = warehouse_item['projected_qty']

        jai_warehouse_item = warehouse_jai.get(box_name, {'warehouse_qty': 0.0})
        jai_warehouse_paper = warehouse_jai.get(paper_name, {'warehouse_qty': 0.0})
        
        amit_warehouse_item = warehouse_amit.get(box_name, {'warehouse_qty': 0.0})
        amit_warehouse_paper = warehouse_amit.get(paper_name, {'warehouse_qty': 0.0})
        
        rana_warehouse_item = warehouse_rana.get(box_name, {'warehouse_qty': 0.0})
        rana_warehouse_paper = warehouse_rana.get(paper_name, {'warehouse_qty': 0.0})
        
        found_paper = next((paper for paper in all_paper if paper['paper'] == paper_name), None)

        if found_paper is not None:
            box['paper'] = found_paper['paper']
            box['jai_paper_stock'] = jai_warehouse_paper.get('warehouse_qty', 0.0)
            box['amit_paper_stock'] = amit_warehouse_paper.get('warehouse_qty', 0.0)
            box['rana_paper_stock'] = rana_warehouse_paper.get('warehouse_qty', 0.0)


        box['production_jai'] = get_box_data(box_name, mr_jai, 'qty')
        box['dispatch_jai'] = po_jai.get(box_name, {'box_qty': 0.0})['box_qty']
        box['po_name_jai'] = po_jai.get(box_name, {'po_name': ''})['po_name']
        box['remain_prod_jai'] = box['production_jai'] - get_box_data(box_name, mr_jai, 'received_qty')
        box['mr_jai'] = get_box_data(box_name, mr_jai, 'mr_name')
        box['stock_jai'] = jai_warehouse_item['warehouse_qty']
        box['priority_jai'] = priority_jai.get(box_name, {'priority': 0})['priority']

        box['production_amit'] = get_box_data(box_name, mr_amit, 'qty')
        box['dispatch_amit'] = po_amit.get(box_name, {'box_qty': 0.0})['box_qty']
        box['po_name_amit'] = po_amit.get(box_name, {'po_name': ''})['po_name']
        box['priority_amit'] = priority_amit.get(box_name, {'priority': 0})['priority']
        box['stock_amit'] = amit_warehouse_item['warehouse_qty']
        box['mr_amit'] = get_box_data(box_name, mr_amit, 'mr_name')
        box['remain_prod_amit'] = box['production_amit'] - get_box_data(box_name, mr_amit, 'received_qty')
        
        box['production_rana'] = get_box_data(box_name, mr_rana, 'qty')
        box['dispatch_rana'] = po_rana.get(box_name, {'box_qty': 0.0})['box_qty']
        box['po_name_rana'] = po_rana.get(box_name, {'po_name': ''})['po_name']
        box['priority_rana'] = priority_rana.get(box_name, {'priority': 0})['priority']
        box['stock_rana'] = rana_warehouse_item['warehouse_qty']
        box['mr_rana'] = get_box_data(box_name, mr_rana, 'mr_name')
        box['remain_prod_rana'] = box['production_rana'] - get_box_data(box_name, mr_rana, 'received_qty')
        

    for box in all_box:
        box['short_qty'] = max(0, (box['so_qty'] + box['msl']) - (box['stock_rapl'] + box['stock_jai'] + box['stock_amit'] + box['production_amit'] + box['production_jai'] + box['production_rana']))
        box['dispatch_need_to_complete_so'] = abs(max(0,  box['rapl_msl'] + box['so_qty'] - box['stock_rapl'] - box['dispatch_amit'] -  box['dispatch_jai'] - box['dispatch_rana']))
        box['total_stock'] = box['stock_amit'] + box['stock_rapl'] + box['stock_jai'] + box['stock_rana']
        box['over_stock_qty'] = min(0, (box['so_qty'] + box['msl']) - (box['stock_rapl'] + box['stock_jai'] + box['stock_amit'] + box['production_amit'] + box['production_jai'] + box['production_rana']))
        box['urgent_dispatch'] = box['so_qty'] - box['stock_rapl']
        
    strategy = SortStrategyFactory.get_strategy(filters.get('report_type'))
    sorted_data = strategy.sort(data=all_box)
    return sorted_data

def priority_cols(builder):
    cols = (builder
        .add_column("J", "Int", 20, "priority_jai")
        .add_column("A", "Int", 20, "priority_amit")
        .add_column("R", "Int", 20, "priority_rana")
        .build()
    )
    return cols

def links_cols(builder):
    cols = (builder
        .add_column("SOs", "HTML", 100, "so_name") 
        .add_column("MR JAI", "HTML", 100, "mr_jai")
        .add_column("MR Amit", "HTML", 100, "mr_amit")
        .add_column("MR Rana", "HTML", 100, "mr_rana")
        .add_column("POs Amit", "HTML", 100, "po_name_amit") 
        .add_column("POs JAI", "HTML", 100, "po_name_jai")
        .add_column("POs Rana", "HTML", 100, "po_name_rana")
        .build()
    )
    return cols

def stock_cols(builder):
    cols = (builder
        .add_column("Rapl Stock", "Int", 80, "stock_rapl")
        .add_column("JAI Stock", "Int", 80, "stock_jai")
        .add_column("Amit Stock", "Int", 80, "stock_amit") 
        .add_column("Total Stock", "Int", 100, "total_stock")
        .build()
    )
    return cols

def prod_cols(builder):
    cols = (builder
        .add_column("JAI Prod", "Int", 80, "production_jai") 
        .add_column("Amit Prod", "Int", 80, "production_amit") 
        .add_column("Rana Prod", "Int", 80, "production_rana")
        .build()
    )
    return cols

def dispatch_cols(builder):
    cols = (builder
        .add_column("Jai Disp", "Int", 80, "dispatch_jai")
        .add_column("Amit Disp", "Int", 80, "dispatch_amit")
        .add_column("Rana Disp", "Int", 80, "dispatch_rana")
        .build()        
    )
    return cols

def common_cols(builder):
    cols = (
        builder
        .add_column("D", "Check", 40, "dead_inventory") 
        .add_column("Item", "Link", 180, "box", options="Item")
        .build()
    )
    return cols

def paper_cols(builder):
    cols = (
        builder
        .add_column("Paper", "Link", 180, "paper", options="Item")
        .add_column("Amit Paper", "Int", 100, "amit_paper_stock", disable_total="True")
        .add_column("Jai Paper", "Int", 100, "jai_paper_stock", disable_total="True")
        .add_column("Rana Paper", "Int", 100, "rana_paper_stock", disable_total="True")
        .build()
    )
    return cols

def urgent_dispatch_column(builder):
    return builder.add_column("Urgent Dispatch", "Int", "urgent_dispatch", "urgent_dispatch")

def dispatch_need_column(builder):
    return builder.add_column("Dispatch Need", "Int", 120, "dispatch_need_to_complete_so")

def shortage_column(builder):
    return builder.add_column("Shortage", "Int", 100, "short_qty")

def so(builder):
    return builder.add_column("SO", "Int", 80, "so_qty").build()

def box_msl(builder):
    return builder.add_column("MSL", "Int", 80, "msl").build()

def rapl_msl(builder):
    return builder.add_column("Rapl MSL", "Int", 80, "rapl_msl").build()

def over_cols(builder):
    return builder.add_column("Over Stock", "Int", 100, "over_stock_qty").build()

def columns(filters=None):
    cols = None
    if filters.get('report_type') == 'Box Stock':
        builder = report_utils.ColumnBuilder()
        cols = common_cols(builder)

    elif filters.get('report_type') == 'Box Production':
        builder = report_utils.ColumnBuilder()
        cols = common_cols(builder)
        cols = box_msl(builder)
        cols = prod_cols(builder)

    elif filters.get('report_type') == 'Box Dispatch':
        builder = report_utils.ColumnBuilder()
        cols = common_cols(builder)
        cols = so(builder)
        cols = rapl_msl(builder)
        cols = dispatch_cols(builder)
        cols = dispatch_need_column(builder)

    elif filters.get('report_type') == 'Dead Stock':
        builder = report_utils.ColumnBuilder()
        cols = common_cols(builder)

    elif filters.get('report_type') == 'Urgent Dispatch':
        builder = report_utils.ColumnBuilder()
        cols = common_cols(builder)
        cols = so(builder)
        cols = urgent_dispatch_column(builder)
        cols = dispatch_cols(builder)

    if filters.get('box_stock'):
        cols = stock_cols(builder)
    if filters.get('paper_stock'):
        cols = paper_cols(builder)
    if filters.get('over_stock'):
        cols = over_cols(builder)
    if filters.get('add_links'):
        cols = links_cols(builder)
    if filters.get('add_priority'):
        cols = priority_cols(builder)
    
    return cols