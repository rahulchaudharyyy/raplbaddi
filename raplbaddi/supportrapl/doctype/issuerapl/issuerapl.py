# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import googlemaps

class IssueRapl(Document):
	def get_sc_address(self):
		return frappe.get_all('Service Centre', ['state', 'district', 'pincode', 'address', 'name'])
	@frappe.whitelist()
	def get_addresses(self):
		gmaps = googlemaps.Client(key='AIzaSyAO5NhknKUS-KUOTjs48mRC9PBAWi2hB70	')
		sc_addresses = []
		for sc in self.get_sc_address():
			sc_address = ''
			for sc in sc.values():
				sc_address = sc
			sc_addresses.append(sc_address)
		chunk_size = 25
		split_sc_addresses = [sc_addresses[i:i + chunk_size] for i in range(0, len(sc_addresses), chunk_size)]
		dms = []
		matrix = {}
		customer_address = " ".join([self.state, self.district, self.pin_code, self.customer_address])
		for sc_address in split_sc_addresses:
			distance_matrix = gmaps.distance_matrix(
				origins=sc_address, destinations=customer_address)
			dms.append(distance_matrix)
		for dm in dms:
			if 'rows' in dm and dm['rows']:
				for i, row in enumerate(dm['rows']):
					if 'elements' in row and row['elements']:
						for j, element in enumerate(row['elements']):
							origin_address = sc_addresses[i]
							if 'status' in element and element['status'] == 'OK':
								distance = int(element['distance']['value']/1000)
								matrix[origin_address] = distance
			options = [{'label': str(value) + ': ' + key, 'value': str(value) + ':' + key, 'km': value} for key, value in matrix.items()]
			options_sorted = sorted(options, key=lambda x: x['km'], reverse=False)
			return options_sorted