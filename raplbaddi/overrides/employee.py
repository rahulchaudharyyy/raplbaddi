import frappe


def autoname(doc, method):
    doc.employee, doc.name = None, None

    if not doc.department:
        frappe.throw("Department is Mandatory")

    department_abbriviation = (
        frappe.get_value("Department", doc.department, "abbriviation")
        or doc.department[:4]
    )
    doc.naming_series = "HR-" + department_abbriviation + "-.####"
    inactive_employee_in_department = frappe.get_list(
        "Employee", filters={"status": "Left"}, pluck="name", order_by="creation desc"
    )
    if inactive_employee_in_department:
        for employee in inactive_employee_in_department:
            active_employee_having_inactive_series = frappe.get_list(
                "Employee",
                filters={"status": "Active", "naming_series": ["like", "%"  + employee + "%"]},
                pluck="name",
            )
            if active_employee_having_inactive_series:
                continue
            else:
                doc.naming_series = employee + "-.#"
