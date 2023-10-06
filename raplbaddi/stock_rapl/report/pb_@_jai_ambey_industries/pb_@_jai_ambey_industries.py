# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count, Sum
from pypika.terms import Case, Not, Field, Order
from frappe.query_builder import AliasedQuery
from raplbaddi.datarapl.doctype.report_full_access_users.report_full_access_users import get_wildcard_users

def permissions():
    pass

def execute(filters=None):
    return columns(filters), data(filters)
   
def data(filters=None):
    
    item = DocType('Item')
    bin = DocType('Bin')
    poi = DocType('Purchase Order Item')
    po = DocType('Purchase Order')
      
    aliased_jai_ambe_po = AliasedQuery('jpo')
    jai_ambey_po_query = frappe.qb.from_(poi).left_join(po).on(po.name == poi.parent).where(po.supplier == "Jai Ambey Industries").where(po.docstatus == 1).select(Sum(poi.qty - poi.received_qty).as_('box_qty'), poi.item_code.as_('box'), Sum(poi.planned_dispatch_qty - poi.received_qty).as_('planned_qty')).groupby(poi.item_code)
    net_po_jai_ambey = negate_null_negative(aliased_jai_ambe_po.box_qty)
    net_dispatch_jai_ambey = negate_null_negative(aliased_jai_ambe_po.planned_qty)
      
    aliased_jai_ambey, jai_ambey_query = AliasedQuery('aliased_jai_ambey'), frappe.qb.from_(bin).where(bin.warehouse == 'Jai Ambey Industries - RAPL').select(bin.item_code, bin.actual_qty)
    jai_ambey_warehouse_qty =  negate_null_negative(aliased_jai_ambey.actual_qty)
    plan_j = negate_null_negative(net_po_jai_ambey - jai_ambey_warehouse_qty)
    
    
    query = (
        frappe.qb
        .from_(item).where(item.item_group == 'Packing Boxes')
        .with_(jai_ambey_po_query, 'jpo').with_(jai_ambey_query, 'aliased_jai_ambey')
        .left_join(aliased_jai_ambe_po).on(aliased_jai_ambe_po.box == item.item_code)
        .left_join(aliased_jai_ambey).on(aliased_jai_ambey.item_code == item.item_code)
        .select(item.name, jai_ambey_warehouse_qty, plan_j, net_dispatch_jai_ambey)
    )
    return query.run()

def negate_null_negative(data: Field) -> Case:
    return (Case().when((data).isnull(), 0)
         .else_(
             Case().when((data) < 0, 0)
                  .else_((data))
         ))

def columns(filters=None):
   cols = [{"label": "item", "fieldtype": "Link", "width": 180, "options": "Item"},
        {"label": "JAI", "fieldtype": "Int", "width": 60},
        {"label": "Prod JAI", "fieldtype": "Int", "width": 100},
        {"label": "Disp JAI", "fieldtype": "Int", "width": 100},
    ]
   return cols