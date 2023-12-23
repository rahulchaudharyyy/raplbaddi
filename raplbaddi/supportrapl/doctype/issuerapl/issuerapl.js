frappe.ui.form.on('IssueRapl', {
	setup(frm) {
		LoadScript()
		add_place_search('page-head-content')
	},
	refresh: function (frm) {
		frappe.Autocomplete($('#places-input'), {})
		add_buttons(frm)
	}
});

function add_place_search() {
	$(".page-head-content").append("<input type='text' id='places-input'>")
}

function LoadScript() {
	var script = document.createElement('script');
	script.src = 'https://maps.googleapis.com/maps/api/js?key=YOURAPIKEY&libraries=places';
	script.async = true;
	script.defer = true;

	script.addEventListener('load', function () {
		frappe.google = new google.maps.places.Autocomplete(document.getElementById('places-input'));
	});

	document.head.appendChild(script);
}

// Custom Buttons
function add_buttons(frm) {
	frm.add_custom_button(__('Set Rates in All Issues'), function () {
		frm.call({
			method: 'set_rates',
			doc: frm.doc,
			callback: function (response) {
			}
		});
	});

	frm.add_custom_button(__('Select SC'), function () {
		frm.call({
			method: 'get_addresses',
			doc: frm.doc,
			callback: function (response) {
				if (response.message) {
					var options = response.message;
					frappe.prompt({
						label: __('Select an Address'),
						fieldname: 'selected_address',
						fieldtype: 'Select',
						options: options,
						reqd: 1,
					},
						(values) => {
							var value = values.selected_address.split(':');
							frm.set_value('service_centre', value[1]);
							frm.set_value('kilometer', value[0]);
						});
				}
			}
		});
	});
}