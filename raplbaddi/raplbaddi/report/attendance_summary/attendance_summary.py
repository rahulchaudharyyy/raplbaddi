# Copyright (c) 2024, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns, datas = [], []
    
    if filters.get('report_type') == "Detailed Attendance":
        datas = attendance_data(filters, detailed=True)
    elif filters.get('report_type') == "Attendance Report":
        datas = attendance_data(filters, detailed=False)
    
    return get_columns(filters), datas

def attendance_data(filters, detailed):
    start_date = filters.get('start_date')
    end_date = filters.get('end_date')
    employee = filters.get('employee')
    shift_type = filters.get('shift_type')

    attendance_records = []
    
    query = f"""
        select
            ar.name,
            ar.date,
            ari.employee,
            ari.employee_name,
            ari.attendance,
            ari.shift_type,
            ari.duration
        from
            `tabAttendance Rapl` ar
            JOIN `tabAttendance Rapl Item` ari on ari.parent = ar.name
        where
            ar.docstatus = 1
            and ar.date between '{start_date}' and '{end_date}'
    """
    
    if employee:
        query += ' and ar.employee = "{}"'.format(employee)
    
    if shift_type:
        query += ' and ari.shift_type = "{}"'.format(shift_type)

    if not detailed:
        query = f"""
            select
                ari.employee,
                ari.employee_name,
                ari.attendance,
                ari.shift_type,
                sum(ari.duration) as total_duration
            from
                `tabAttendance Rapl` ar
                JOIN `tabAttendance Rapl Item` ari on ari.parent = ar.name
            where
                ar.docstatus = 1
                and ar.date between '{start_date}' and '{end_date}'
        """
        
        if employee:
            query += ' and ar.employee = "{}"'.format(employee)
        
        if shift_type:
            query += ' and ari.shift_type = "{}"'.format(shift_type)

        query += """
            group by ari.employee
        """
    
    attendance_records = frappe.db.sql(query, as_dict=True)

    data = []
    for record in attendance_records:
        if detailed:
            data.append({
                "Employee": record.employee_name,
                "Date": record.date,
                "Duration": record.duration,
                "Attendance": record.attendance,
                "Shift Type": record.shift_type
            })
        else:
            data.append({
                "Employee": record.employee_name,
                "Date": None,
                "Duration": record.total_duration,
                "Attendance": record.attendance,
                "Shift Type": record.shift_type
            })
    return data

def get_columns(filters):
    return [
        {"label": "Employee Name", "fieldname": "Employee", "fieldtype": "Link", "options": "Employee"},
        {"label": "Date", "fieldname": "Date", "fieldtype": "Date"},
        {"label": "Duration", "fieldname": "Duration", "fieldtype": "Duration"},
        {"label": "Attendance", "fieldname": "Attendance", "fieldtype": "Select"},
        {"label": "Shift Type", "fieldname": "Shift Type", "fieldtype": "Link", "options": "Shift Type"}
    ]
