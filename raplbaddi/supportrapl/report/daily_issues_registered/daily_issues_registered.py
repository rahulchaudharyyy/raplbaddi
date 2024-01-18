# Copyright (c) 2024, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
class dailyIssue:
	def __init__(self,filters) :
		self.filters = filters
		self.get_data()
		self.convert_date()
  
	def get_columns(self,filters):
		columns = [
			{
					"fieldname": "complaint_no",
					"label": ("Complaint No."),
					"fieldtype": "Link",
					"options": "IssueRapl",
					"width": 400,
				},
			{
					"fieldname": "service_centre",
					"label": ("Service Centre"),
					"fieldtype": "Link",
					"options": "Service Centre",
					"width": 500,
				},
			{
					"fieldname": "creation",
					"label": ("Date"),
					"fieldtype": "Date",
					"width": 400,
				}
		]
		return columns

	def convert_date(self):
		self.filters.start_date = datetime.strptime(self.filters.start_date, "%Y-%m-%d").date()
		return self.filters
	def get_data(self):
		self.query = f"""
        select 
			name as 'complaint_no',
			service_centre AS service_centre,
			DATE(creation) AS creation
        from tabIssueRapl
        """
		self.result = frappe.db.sql(self.query, as_dict=True)
		print(self.result[0])
  
	def filtred_data(self):
		self.filtered_data = []
		data = self.result
		print(self.filters.start_date)
		for i in data:
			if not self.filters.start_date or i.creation == self.filters.start_date:
				self.filtered_data.append(i)
		return self.filtered_data
    
	def get_msg(self):
		self.count = len(self.filtered_data)
		
		return f"""<h1 style="text-align:center;color:Orange" >No. of Issues Registered Today are : {self.count}</h1>"""
		

def execute(filters=None):
    issue = dailyIssue(filters)
    columns, data = [], []
    return issue.get_columns(filters), issue.filtred_data(),issue.get_msg()







