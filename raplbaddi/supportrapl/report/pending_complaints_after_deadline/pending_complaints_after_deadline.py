# Copyright (c) 2024, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe

class daysDeadline():
	def __init__(self,filters):
		self.countComplaints()
		self.get_data()
  
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
				DATEDIFF(CURDATE(),custom_creation_date) >3

		"""
		self.result = frappe.db.sql(query, as_dict=True)
		return self.result

	def get_columns(self,filters):
		columns = [
			{
				'fieldname':'name',
				'label':'Complaint No',
				'fieldtype':'Link',
				'options':'IssueRapl',
				'width':'300'
			},
			{
				'fieldname':'custom_creation_date',
				'label':'Complaint Register Date',
				'fieldtype':'Date',
				'width':'310'
			},
			{
				'fieldname':'today',
				'label':'Current Day',
				'fieldtype':'Date',
				'width':'280'
			},
			{
				'fieldname':'days_diff',
				'label':'Date Difference',		
				'fieldtype':'Int',
				'width':'250'
			}
		]
		return columns

	def countComplaints(self):
		data = self.get_data()
		self.count = 0
		for i in data:
			self.count+=1
  
	def get_msg(self):
		return f'''
			<h1 style = 'text-align:center; color:orange;'>No. of pending complaints after deadline are : {self.count} </h1>
  		'''

  
def execute(filters=None):
	deadline = daysDeadline(filters)
	deadline.countComplaints()
	columns, data = [], []
	return deadline.get_columns(filters), deadline.get_data(), deadline.get_msg()

