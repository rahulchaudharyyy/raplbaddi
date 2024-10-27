import frappe
import calendar

def execute(filters=None):
    columns = get_columns()
    datas = get_attendance_data(filters)
    return columns, datas

def get_attendance_data(filters):
    return attendance_data(filters, detailed=(filters.get('report_type') == "Detailed Attendance"))

def attendance_data(filters, detailed):
    start_date, end_date = filters.get('start_date'), filters.get('end_date')
    employee, shift_type = filters.get('employee'), filters.get('shift_type')
    query = build_attendance_query(start_date, end_date, employee, shift_type)
    attendance_records = frappe.db.sql(query, as_dict=True)
    data = add_salary_to_data(attendance_records)
    if not detailed:
        data = consolidate_records(data)
    return data

def consolidate_records(data):
    consolidated = {}
    
    for record in data:
        employee = record['Employee']
        
        if employee not in consolidated:
            consolidated[employee] = {
                'Attendance': record['Attendance'],
                'Duration': record['Duration'],
                'Shift Type': record['Shift Type'],
                'Total Salary': record['Salary']
            }
        else:
            consolidated[employee]['Duration'] += record['Duration']
            consolidated[employee]['Total Salary'] += record['Salary']

    consolidated_list = [
        {
            'Employee': employee,
            'Attendance': details['Attendance'],
            'Duration': details['Duration'],
            'Shift Type': details['Shift Type'],
            'Salary': details['Total Salary']
        }
        for employee, details in consolidated.items()
    ]

    return consolidated_list

def build_attendance_query(start_date, end_date, employee, shift_type):
    query = f"""
        SELECT
            ar.name,
            ar.date,
            ari.employee,
            ari.employee_name,
            ari.attendance,
            ari.shift_type,
            ari.duration
        FROM
            `tabAttendance Rapl` ar
            JOIN `tabAttendance Rapl Item` ari ON ari.parent = ar.name
        WHERE
            ar.docstatus = 1
            AND ar.date BETWEEN '{start_date}' AND '{end_date}'
    """
    
    if employee:
        query += f' AND ar.employee = "{employee}"'
    
    if shift_type:
        query += f' AND ari.shift_type = "{shift_type}"'

    return query

def add_salary_to_data(attendance_records):
    data = []
    for record in attendance_records:
        hourly_rate = get_hourly_rate(record.employee, record.date)
        salary = (record.duration/3600 or 0) * hourly_rate
        entry = {
            "Employee": record.employee_name,
            "Date": record.date,
            "Duration": record.duration,
            "Attendance": record.attendance,
            "Shift Type": record.shift_type,
            "Hourly Rate": hourly_rate,
            "Salary": salary
        }
        data.append(entry)
    return data

def get_monthly_salary_dict_employee(employee, year):
    salary_doc = frappe.get_doc("Employee Salary", f"{employee} {year}")
    return salary_doc.items if salary_doc else []

def get_hourly_rate(employee, date):
    year, month = date.year, date.strftime("%B")
    salary_items = get_monthly_salary_dict_employee(employee, year)
    monthly_salary = {item.month: item.value for item in salary_items}
    
    if not monthly_salary:
        return 0.0

    days_in_month = calendar.monthrange(year, date.month)[1]
    return monthly_salary.get(month, 0.0) / days_in_month if days_in_month else 0.0

def get_columns():
    return [
        {"label": "Employee Name", "fieldname": "Employee", "fieldtype": "Link", "options": "Employee"},
        {"label": "Date", "fieldname": "Date", "fieldtype": "Date"},
        {"label": "Duration", "fieldname": "Duration", "fieldtype": "Duration"},
        {"label": "Attendance", "fieldname": "Attendance", "fieldtype": "Select"},
        {"label": "Shift Type", "fieldname": "Shift Type", "fieldtype": "Link", "options": "Shift Type"},
        {"label": "Hourly Rate", "fieldname": "Hourly Rate", "fieldtype": "Currency"},
        {"label": "Salary", "fieldname": "Salary", "fieldtype": "Currency"}
    ]