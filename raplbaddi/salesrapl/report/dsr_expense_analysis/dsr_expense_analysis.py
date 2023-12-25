# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	return get_columns(), get_data()

def get_columns():
    columns = [
			{'fieldname': 'name','label': ('Sales_Person'),'fieldtype': 'Data'},
			{'fieldname': 'party_name','label': ('Party Name'),'fieldtype': 'Data'},
			{'fieldname': 'district','label': ('Place Of Visit'),'fieldtype': 'Data'},
			{'fieldname':'type','label':('Type of Expense'),'fieldtype': 'Data'},
			{'fieldname':'remarks','label':('Remarks'),'fieldtype': 'Data'},
			{'fieldname':'date_of_visit','label':('Date Of Visted'),'fieldtype': 'Date'},
			{'fieldname':'amount','label':('Amount'),'fieldtype': 'Int'},
			{'fieldname':'visits','label':('No of times Visited'),'fieldtype':'Int'}		 
		]
    return columns

    
    
def get_data():
    query = '''
    WITH FirstJoin AS (
        SELECT
            DSL.parent,
            DSRA.date as date,
            DSL.party_name,
            DSL.district,
            DSL.remarks,
            1 AS Visit
        FROM
            `tabDaily Sales Report By Admin` AS DSRA
            JOIN `tabDaily Sales Lead` AS DSL ON DSRA.name = DSL.parent
    )
    SELECT
        SUBSTRING_INDEX(fs.parent,' ',2) AS name,
        fs.party_name,
        fs.district,
        DSE.type,
        fs.date AS date_of_visit,
        fs.remarks,
        DSE.amount,
        1 AS visits
    FROM
        FirstJoin AS fs
        JOIN `tabDaily Sales Expenses By Admin` AS DSE ON DSE.parent = fs.parent
    '''
    result = frappe.db.sql(query, as_dict=True)
    print(result)
    return result
