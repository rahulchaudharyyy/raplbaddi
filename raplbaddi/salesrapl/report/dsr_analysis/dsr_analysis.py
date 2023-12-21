# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt
import frappe
from datetime import datetime
from frappe.utils import dateutils

def execute(filters=None):
	columns, data = [], []
	return get_columns(), get_filtered_data(filters)

# Use to get the columns
def get_columns():
	columns = [
			{'fieldname': 'Sales_Person','label': ('Sales_Person'),'fieldtype': 'Data'},
			{'fieldname': 'party','label': ('Party Name'),'fieldtype': 'Data'},
			{'fieldname': 'date','label': ('Date Of Visit'),'fieldtype': 'Date'},
			{'fieldname':'Remarks','label':('Remarks'),'fieldtype': 'Data'},
			{'fieldname':'Visit','label':('No of times Visited'),'fieldtype':'Int'}		 
		]
	return columns

# Gives the dataset after executing the query...
def get_data():						
    query = f"""
	SELECT  SUBSTRING_INDEX(DSRA.name,' ',2) AS Sales_Person,
	DSL.party_name as party,
	DSRA.date as date,
	DSL.remarks as Remarks,
	1 as Visit
	from  `tabDaily Sales Report By Admin` as DSRA
	JOIN `tabDaily Sales Lead` as DSL ON DSRA.name = DSL.parent 
	ORDER BY Sales_Person ASC
			"""
    result = frappe.db.sql(query, as_dict=True)
    print(result[0]['date'])
    return result

# Convert the date in date format from string
def convert_date(date_str):
     return datetime.strptime(str(date_str), '%Y-%m-%d').date() if date_str else None


def get_filtered_data(filters):
	data = get_data()
	if not filters:
		return data
	return apply_filters(filters, data)

def apply_filters(filters, data):
    return_data = []
    start_date, end_date, sales_person = get_filters(filters)
    for row in data:
    	if (not sales_person or row['Sales_Person'] == sales_person) and (not start_date or convert_date(row['date']) >= start_date) and (not end_date or convert_date(row['date']) <= end_date):
            return_data.append(row)
    return return_data


def get_filters(filters):
	start_date = convert_date(filters.get('start_date')) if filters.get('start_date') else datetime.now().date()
	end_date = convert_date(filters.get('end_date')) if filters.get('end_date') else datetime.now().date()
	sales_person = filters.get('sales_person') if filters.get('sales_person') else None
	print(start_date)
	print(end_date)
	return start_date,end_date,sales_person
 
 
 
 
 