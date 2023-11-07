# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests

class IssueRapl(Document):
    def validate(self):
        api_key = 'AIzaSyAO5NhknKUS-KUOTjs48mRC9PBAWi2hB70'
        customer_address = self.customer_address + self.district + self.state + self.pin_code
        service_centre = frappe.get_doc('Service Centre', self.service_centre)
        service_centre_address = service_centre.address + service_centre.district + service_centre.pincode + service_centre.state + service_centre.country
        url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={service_centre_address}&destinations={customer_address}&key={api_key}'
        response = requests.get(url=url)
        if response.status_code == 200:
            data = response.json()
            self.kilometer = (data.get('rows')[0].get('elements')[0].get('distance').get('value')/1000)
        else:
            frappe.throw(f"Error: {response.status_code} - {response.text}")
    