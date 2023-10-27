# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.utils import cint
from raplbaddi.datarapl.doctype.report_full_access_users.report_full_access_users import permission_decorator

def execute(filters=None):
	if not filters:
		filters = {}

	days_since_last_order = filters.get("days_since_last_order")
	doctype = filters.get("doctype")

	if cint(days_since_last_order) <= 0:
		frappe.throw(_("'Days Since Last Order' must be greater than or equal to zero"))

	columns = get_columns()
	customers = run(filters, doctype)
	print(customers)

	data = []
	if customers:
		for cust in customers:
			if cint(cust[8]) >= cint(days_since_last_order):
				cust.insert(7, get_last_sales_amt(cust[0], doctype))
				data.append(cust)
	return columns, data

def run(filters, doctype):
	@permission_decorator(doc='Customer Group', value='Navdeep Singla', user='navi.singla123@gmail.com')
	def get_sales_details(doctype):
		cond = """sum(so.base_net_total) as 'total_order_considered',
				max(so.posting_date) as 'last_order_date',
				DATEDIFF(CURRENT_DATE, max(so.posting_date)) as 'days_since_last_order' """
		if doctype == "Sales Order":
			cond = """sum(if(so.status = "Stopped",
					so.base_net_total * so.per_delivered/100,
					so.base_net_total)) as 'total_order_considered',
				max(so.transaction_date) as 'last_order_date',
				DATEDIFF(CURRENT_DATE, max(so.transaction_date)) as 'days_since_last_order'"""

		return frappe.db.sql(
			"""select
				cust.name,
				cust.customer_name,
				cust.territory,
				cust.customer_group,
				count(distinct(so.name)) as 'num_of_order',
				sum(base_net_total) as 'total_order_value', {0}
			from `tabCustomer` cust, `tab{1}` so
			where cust.name = so.customer and so.docstatus = 1 and cust.customer_group = '{2}'
			group by cust.name
			order by 'days_since_last_order' desc """.format(
				cond, doctype, filters.get('sales_person')
			),
			as_list=1,
		)
	return get_sales_details(doctype)

def get_last_sales_amt(customer, doctype):
	cond = "posting_date"
	if doctype == "Sales Order":
		cond = "transaction_date"
	res = frappe.db.sql(
		"""select base_net_total from `tab{0}`
		where customer = %s and docstatus = 1 order by {1} desc
		limit 1""".format(
			doctype, cond
		),
		customer,
	)

	return res and res[0][0] or 0


def get_columns():
	return [
		_("Customer") + ":Link/Customer:120",
		_("Customer Name") + ":Data:120",
		_("Territory") + "::120",
		_("Customer Group") + "::120",
		_("Number of Order") + "::120",
		_("Total Order Value") + ":Currency:120",
		_("Total Order Considered") + ":Currency:160",
		_("Last Order Amount") + ":Currency:160",
		_("Last Order Date") + ":Date:160",
		_("Days Since Last Order") + "::160",
	]
