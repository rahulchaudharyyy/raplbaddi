import frappe
from raplbaddi.utils import report_utils
from pypika import Case

def sre():
	sre = frappe.qb.DocType("Stock Reservation Entry")
	query = (
		frappe.qb.from_(sre)
		.select((sre.reserved_qty - sre.delivered_qty).as_('reserved_qty'), sre.warehouse.as_('warehouse'), sre.item_code.as_('item_code'), sre.voucher_no.as_('sales_order'), sre.voucher_detail_no.as_('sales_order_item'))
		.where(
			(sre.docstatus == 1)
			& (sre.reserved_qty >= sre.delivered_qty)
			& (sre.status.notin(["Delivered", "Cancelled"]))
		)
	)
	ret = query.run(as_dict=True)
	return ret

def soi():
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
			soi.name.as_('sales_order_item'),
			so.status.as_('status'),
			so.customer.as_('customer'),
			so.conditions.as_('so_remarks'),
			soi.custom_box.as_('box'),
			so.planning_remarks.as_('planning_remarks'),
			so.name.as_('sales_order'),
			soi.item_code.as_('item_code'),
			report_utils.Greatest(0, soi.qty - soi.delivered_qty).as_('pending_qty'),
			(soi.stock_reserved_qty).as_('stock_reserved_qty'),
			soi.warehouse.as_('brand'),
			so.delivery_status.as_('delivery_status')
		)
	)	
	data = query.run(as_dict=True)
	return data

def bin():
	bin = frappe.qb.DocType('Bin')
	query = (
		frappe.qb
		.from_(bin)
		.select(bin.item_code, bin.warehouse, bin.actual_qty)
		.where(bin.item_code.like('G%%'))
	)
	return query.run(as_dict=True)

def box():
    from raplbaddi.stock_rapl.report.pb_report.box_data import BoxRequirements
    box = BoxRequirements()
    box_qty = box.warehouse_qty(warehouse='Packing Boxes - RAPL')
    return box_qty