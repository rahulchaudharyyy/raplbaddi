from erpnext.controllers.queries import get_fields, get_filters_cond, get_match_cond, frappe

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def billing_rule(doctype, txt, searchfield, start, page_len, filters):
	doctype = "Billing Rule Rapl"
	conditions = []
	fields = get_fields(doctype, ["name"])

	return frappe.db.sql(
		"""select {fields}
		from `tabBilling Rule Rapl`
		where `tabBilling Rule Rapl`.disabled=0
			and `tabBilling Rule Rapl`.`{key}` like %(txt)s
			{fcond} {mcond}
		order by
			(case when locate(%(_txt)s, name) > 0 then locate(%(_txt)s, name) else 99999 end),
			idx desc, name
		limit %(page_len)s offset %(start)s""".format(
			fields=", ".join(fields),
			fcond=get_filters_cond(doctype, filters, conditions).replace("%", "%%"),
			mcond=get_match_cond(doctype).replace("%", "%%"),
			key=searchfield,
		),
		{
			"txt": "%" + txt + "%",
			"_txt": txt.replace("%", ""),
			"start": start or 0,
			"page_len": page_len or 20,
		},
	)