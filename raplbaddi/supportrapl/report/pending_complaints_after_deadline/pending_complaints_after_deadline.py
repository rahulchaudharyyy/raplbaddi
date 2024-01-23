# Copyright (c) 2024, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe

class daysDeadline():
	def __init__(self,filters):
		self.filters = filters
		self.get_data()
		self.count = 0
  
	def get_data(self):
		query = f"""
			SELECT 
				name,
				custom_creation_date ,
				CURDATE() as 'today',
				DATEDIFF(CURDATE(),custom_creation_date) as 'days_diff'
			FROM 
				tabIssueRapl
			WHERE 
				DATEDIFF(CURDATE(),custom_creation_date) >3 AND service_delivered = "No"

		"""
		group_by_query = f"""
			SELECT 
				custom_creation_date ,
				count(name) as 'no_of_complaints'
			FROM 
				tabIssueRapl
			WHERE 
				DATEDIFF(CURDATE(),custom_creation_date) >3 AND service_delivered = "No"
			GROUP BY 
				custom_creation_date
  
  		"""
    
		result = frappe.db.sql(query, as_dict=True)
		self.count = len(result)   
		self.group_by_result = frappe.db.sql(group_by_query,as_dict = True)
		# getting the group_by_date filter
		self.filters.group_by_date = self.filters.group_by_date
		data = self.group_by_result if self.filters.group_by_date else result
		return data

	def get_columns(self,filters):
		columns = [
			{
				'fieldname':'custom_creation_date',
				'label':'Complaint Register Date',
				'fieldtype':'Date',
				'width':'310'
			},
			{
				'fieldname':'no_of_complaints',
				'label':'No of Complaints',		
				'fieldtype':'Int',
				'width':'250'
			}
		]
		return columns

	def get_msg(self):
		return f'''
			<h1 style = 'text-align:center; color:orange;'>No. of pending complaints after deadline are : {self.count} </h1>
  		'''

  
def execute(filters=None):
	deadline = daysDeadline(filters)
	columns, data = [], []
	return deadline.get_columns(filters), deadline.get_data(),deadline.get_msg()

