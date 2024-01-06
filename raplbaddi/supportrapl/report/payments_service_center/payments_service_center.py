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
		SUBSTRING_INDEX(CASE WHEN i.custom_creation_date THEN i.custom_creation_date ELSE i.creation END ," ",1) as 'Date', 
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
		{'fieldname': 'complaint_no','label': ('Complaint No.'),'fieldtype': 'Link','options':'IssueRapl','width':300},
		{'fieldname': 'Date','label': ('Date'),'fieldtype': 'Date','width':300},
		{'fieldname': 'Service Center','label': ('Service Center'),'fieldtype': 'Link','options':'Service Centre','width':300},
		{'fieldname': 'KMs','label': ('KMs'),'fieldtype': 'Data','width':150},
		{'fieldname': 'Amount','label': ('Amount'),'fieldtype': 'Data','width':137}
		]
		return columns
    
    	
	def get_filtered_data(self):
		self.start_date = self.filters.get('start_date')
		self.end_date = self.filters.get('end_date')
		self.service_centre = self.filters.get('Service_Centre')
		self.get_data()
		self.filtered_data = []
		for i in self.data:
			if (not self.service_centre or i.get('Service Center') == self.service_centre)and(not self.start_date or i.get('Date','2024-01-01') >= self.start_date) and (not self.end_date or i.get('Date','2024-01-01') <= self.end_date):
				self.filtered_data.append(i)
		return self.filtered_data

	def get_count(self):
		self.counts = len(self.filtered_data)

	def get_total_amount(self):
		self.ret = 0
		for data in self.filtered_data:
			self.ret += data.Amount
		self.payment = int(self.ret)

	
	def get_account_details(self):
		if self.filters.Service_Centre:
			self.account_no = self.filtered_data[0]['Account No.']
			self.bank_ifsc = self.filtered_data[0]['Bank IFSC']
			self.bank_name = self.filtered_data[0]['Bank']
			self.upi = self.filtered_data[0]['UPI Id']
   
		else:
			self.account_no,self.bank_ifsc,self.bank_name,self.upi = None,None,None,None
	

	def get_msg(self):
		self.get_count()
		self.get_total_amount()
		self.get_account_details()
		return f"""
		<div style="display: flex; justify-content: space-between;">
			<h2>Complaints : {self.counts}</h2>
			<h2> {self.service_centre}</h2>
			<h2>Amount : {self.payment}</h2>
		</div> <br>
		<div style="display: flex; justify-content: space-between;">
			<h4>Bank : {self.bank_ifsc}</h4>
			<h4>Account No : {self.account_no}</h4>
			<h4>IFSC : {self.bank_name}</h4>
			<h4>UPI Id : {self.upi}</h4>
		</div>
		"""


def execute(filters=None):
	payment = PayementReport(filters)
	columns, data = [], []
	return payment.get_columns(), payment.get_filtered_data(),payment.get_msg()


