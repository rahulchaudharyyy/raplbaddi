import frappe

@frappe.whitelist()
def get_customer_details(customer):
    return frappe.db.sql(f"""
        SELECT customer_address, customer_phone_number, serial_no, brand, model
        FROM `tabSupport Customer`
        WHERE name='{customer}'
    """, as_dict=True)

@frappe.whitelist()
def get_dpi_parent(sno):
       return frappe.db.sql(f"""
        SELECT parent FROM `tabDaily Production Item` as dpi
        WHERE dpi.name='{sno}'
    """, as_dict=True)

@frappe.whitelist()
def get_last_so_of_customer(customer=None):
    filter =  {'customer': customer}
    try:
        so = frappe.get_last_doc('Sales Order', filters=filter)
        return so
    except:
        return "Doc not found"

@frappe.whitelist()
def price_list_of_customer(customer=None):
    try:
        price_list = frappe.db.sql(f"""
            SELECT soi.item_code, soi.rate, soi.discount_amount, MAX(so.transaction_date) AS latest_transaction_date
            FROM `tabSales Order Item` AS soi
            JOIN `tabSales Order` AS so ON so.name = soi.parent
            WHERE so.customer = '{customer}' AND so.docstatus = 1
            GROUP BY so.customer, soi.item_code
        """, as_dict=True
        )
        return price_list
    except:
        return "Doc not Found"

@frappe.whitelist()
def get_task(user=None, frequency=None):
    try:
        task = frappe.db.sql(f"""
            SELECT name
            FROM `tabTask Rapl`
            WHERE '{user}' IN (user_kaccha, user_pakka, user_assistant) AND frequency = '{frequency}';
        """, as_dict=True
        )
        return task
    except:
        return "No Task Found"


def get_fields(doctype, fields=None):
    from frappe.utils import unique
    if fields is None:
        fields = []
    meta = frappe.get_meta(doctype)
    fields.extend(meta.get_search_fields())

    if meta.title_field and not meta.title_field.strip() in fields:
        fields.insert(1, meta.title_field.strip())

    return unique(fields)

from frappe.desk.reportview import get_filters_cond, get_match_cond
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def bom(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
    doctype = "Purchase Order"
    print(txt)
    conditions = []   
    q = """SELECT poi.item_code as item_code, SUM(poi.qty - poi.received_qty) as received_qty
                FROM `tabPurchase Order Item` AS poi
                JOIN `tabPurchase Order` ON `tabPurchase Order`.name = poi.parent
                WHERE 1
                    {fcond} {mcond}
                    AND poi.item_code LIKE %(txt)s
                    AND poi.qty - poi.received_qty > 0
                GROUP BY
                    poi.item_code
                ORDER BY
                    poi.qty - poi.received_qty DESC
                LIMIT {start}, {page_len}              
                """.format(
                **{
                    "key": searchfield,
                    "fcond": get_filters_cond(doctype, filters, conditions),
                    "mcond": get_match_cond(doctype),
                    "start": start,
                    "page_len": page_len,
                }
            )
    return frappe.db.sql(
        q, {"txt": "%%%s%%" % txt}, as_dict=as_dict)
    
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def customer_query(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
    print(txt)
    doctype = "Customer"
    conditions = []
    cust_master_name = frappe.defaults.get_user_default("cust_master_name")

    fields = ["name"]
    if cust_master_name != "Customer Name":
        fields.append("customer_name")

    fields = get_fields(doctype, fields)
    searchfields = frappe.get_meta(doctype).get_search_fields()
    searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)
    return frappe.db.sql(
        """select {fields} from `tabCustomer`
        where docstatus < 2
            and ({scond}) and disabled=0
            {fcond} {mcond}
        order by
        	(case when locate({txt}, name) > 0 then locate({txt}, name) else 99999 end),
        	(case when locate({txt}, customer_name) > 0 then locate({txt}, customer_name) else 99999 end),
        	idx desc,
        	name, customer_name
        limit %(page_len)s offset %(start)s""".format(
            **{
                "fields": ", ".join(fields),
                "scond": searchfields,
                "mcond": get_match_cond(doctype),
                "fcond": get_filters_cond(doctype, filters, conditions).replace("%", "%%"),
            }
        ),
        {"txt": "%%%s%%" % txt, "_txt": txt.replace("%", ""), "start": start, "page_len": page_len},
        as_dict=as_dict,
    )