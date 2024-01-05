# Copyright (c) 2024, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
class PayementReport:
	def __init__(self, filters):
		self.filters = filters

	def get_data(self):						
		query = f"""
		select 
		i.name AS complaint_no,
		SUBSTRING_INDEX(i.custom_creation_date," ",1) as 'Date', 
		j.service_centre_name as 'Service Center',
		j.bank_name as 'Bank',
		j.bank_account_no as 'Account No.',
		j.ifsc_code as 'Bank IFSC',
		j.upi_id as 'UPI Id',
		i.kilometer as 'KMs',
		i.amount as 'Amount'
		from tabIssueRapl as i
		inner Join 
		`tabService Centre` as j on i.service_centre = j.service_centre_name
		where i.service_delivered = 'Yes'
		"""
		
		result = frappe.db.sql(query, as_dict=True)
		
		self.data = result
        
	def get_columns(self):
		columns = [
		{'fieldname': 'complaint_no','label': ('Complaint No.'),'fieldtype': 'Link','options':'IssueRapl'},
		{'fieldname': 'Date','label': ('Date'),'fieldtype': 'Date'},
		{'fieldname': 'Service Center','label': ('Service Center'),'fieldtype': 'Link','options':'Service Centre'},
		{'fieldname': 'Bank','label': ('Bank Name'),'fieldtype': 'Data'},
		{'fieldname': 'Account No.','label': ('Account No.'),'fieldtype': 'Data'},
		{'fieldname': 'Bank IFSC','label': ('IFSC Code'),'fieldtype': 'Data'},
		{'fieldname': 'UPI Id','label': ('UPI Id'),'fieldtype': 'Data'},
		{'fieldname': 'KMs','label': ('Kilometers'),'fieldtype': 'Data'},
		{'fieldname': 'Amount','label': ('Amount'),'fieldtype': 'Data'}

		]
		return columns
    	
	def get_filtered_data(self):
		start_date = self.filters.get('start_date')
		end_date = self.filters.get('end_date')
		service_centre = self.filters.get('Service_Centre')
		self.get_data()
		filterd_data = []
		for i in self.data:
			if (not service_centre or i['Service Center'] == service_centre)and(not start_date or i['Date'] >= start_date) and (not end_date or i['Date'] <= end_date):
				filterd_data.append(i)
		return filterd_data



def execute(filters=None):
	payment = PayementReport(filters)
	columns, data = [], []
	return payment.get_columns(), payment.get_filtered_data()
