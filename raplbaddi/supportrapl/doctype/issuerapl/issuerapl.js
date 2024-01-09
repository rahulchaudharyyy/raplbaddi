class IssueRaplForm {
	constructor(frm) {
		this.frm = frm;
		this.placeInputId = '#places-input'
		this.placeInput = $(this.placeInputId)
	}

	setup() {
		$("#form-tabs").append(`<input type='text' id='${this.placeInputId}' style='width: 700px; height: 40px;'>`);
		this.getGoogleApiKey();
		this.addButtons()
	}

	getGoogleApiKey() {
		frappe.db.get_single_value('Google Settings', 'api_key')
			.then(apiKey => {
				if (apiKey) {
					this.apiKey = apiKey;
					this.loadScript();
				} else {
					console.error("Google API key is not set in 'Google Settings'.");
				}
			});
	}

	loadScript() {
		let script = document.createElement('script');
		script.src = `https://maps.googleapis.com/maps/api/js?key=${this.apiKey}&libraries=places`;
		script.async = true;
		script.defer = true;

		script.addEventListener('load', () => this.handleScriptLoad());
	}
	handleScriptLoad() {
		console.log('In script')
		frappe.google = new google.maps.places.Autocomplete(document.getElementById(this.placeInput), { componentRestrictions: { country: "in" } });
		frappe.google.addListener('place_changed', () => this.handlePlaceChanged());
	}

	handlePlaceChanged() {
		let frm = this.frm;
		frm.selectedPlace = frappe.google.getPlace();
		frm.set_value('customer_address', frm.selectedPlace.formatted_address);
	}

	addButtons() {
		this.frm.add_custom_button(__('Select SC'), () => {
			this.frm.call({
				method: 'get_addresses',
				doc: this.frm.doc,
				callback: response => this.handleAddressResponse(response)
			});
		});
	}

	handleAddressResponse(response) {
		if (response.message) {
			let options = response.message;
			this.showAddressPrompt(options);
		}
	}

	showAddressPrompt(options) {
		frappe.prompt({
			label: __('Select an Address'),
			fieldname: 'selected_address',
			fieldtype: 'Select',
			options: options,
			reqd: 1,
		}, values => this.setServiceCentreValue(values.selected_address));
	}

	setServiceCentreValue(selectedAddress) {
		let value = selectedAddress.split(':');
		this.frm.set_value('service_centre', value[0]);

		this.frm.call({
			method: 'set_kilometers',
			doc: this.frm.doc,
			args: {
				service_centre: value[0],
				aerial: value[1]
			},
			callback: () => {
				console.log(this.frm.doc.kilometer);
				this.frm.save()
			}
		});
	}
}

frappe.ui.form.on('IssueRapl', {
	refresh: frm => new IssueRaplForm(frm).setup(),
});