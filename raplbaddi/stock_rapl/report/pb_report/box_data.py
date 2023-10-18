from frappe.query_builder import DocType
from frappe.query_builder.functions import Concat, Sum, GroupConcat, Coalesce, Case
from frappe.utils import get_url
from raplbaddi.utils import report_utils
import frappe

def all_boxes() -> dict:
    items = DocType('Item')
    box_query = (
        frappe.qb
        .from_(items)
        .where(items.item_group == "Packing Boxes").where(items.disabled == 0)
        .select(items.name.as_('box'), items.safety_stock.as_('msl'))
    )
    return box_query.run(as_dict=True)

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
    return report_utils.remove_negative(['warehouse_qty'], qty_query.run(as_dict=True))

def get_box_requirement_from_so() -> dict:
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
    return so_query.run(as_dict=True)

def get_box_order_for_production(supplier):
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

def get_supplier_priority():
    psp = DocType('Paper Supplier Priority')
    pp_query = (
        frappe.qb
        .from_(psp)
        .select(
            psp.paper_name, psp.supplier, psp.priority, psp.parent
        )
    )
    print(report_utils.accum_mapper(data=pp_query.run(as_dict=True), key='parent'))