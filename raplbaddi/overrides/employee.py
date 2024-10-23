import frappe


def autoname(doc, method):
    doc.employee, doc.name = None, None

    if not doc.department or doc.branch == None:
        frappe.throw("Department and branch is Mandatory")

    department_abbriviation = (
        frappe.get_value("Department", doc.department, "abbriviation")
        or doc.department[:3]
    )

    branch_name = doc.branch
    if doc.branch == "Real Appliances Private Limited":
        branch_name = "RAPL"
    elif doc.branch == "Red Star Unit 2":
        branch_name = "RSI"

    doc.naming_series = "E-" + branch_name + "-" + department_abbriviation + "-.#"
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
