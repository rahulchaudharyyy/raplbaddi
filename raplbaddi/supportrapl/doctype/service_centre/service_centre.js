frappe.ui.form.on('Service Centre', {
    setup(frm) {
        get_google_api_key(frm);
        add_elements();
    },
    refresh: function (frm) {
        add_buttons(frm);
    },
	after_save: function(frm) {
		$('#places-input').val('')
	}
});


function add_elements() {
    $("#form-tabs").append("<input type='text' id='places-input' style='width: 700px; height: 40px;'>");
}

function get_google_api_key(frm) {
    frappe.db.get_single_value('Google Settings', 'api_key')
        .then(r => {
            LoadScript(r, frm);
        });
}

function LoadScript(api_key, frm) {
    let script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${api_key}&libraries=places`;
    script.async = true;
    script.defer = true;

    script.addEventListener('load', function () {
        frappe.google = new google.maps.places.Autocomplete(document.getElementById('places-input'));
        frappe.google.addListener('place_changed', function () {
            frm.selectedPlace = frappe.google.getPlace();
			console.log
			let state = ""
			frm.selectedPlace.address_components.forEach( r => {
				if(r.types.includes("administrative_area_level_1")) {
					state = r.long_name
				}
			})
			frm.set_value('latitude', frm.selectedPlace.geometry.location.lat())
			frm.set_value('longitude', frm.selectedPlace.geometry.location.lng())
			frm.set_value('address', frm.selectedPlace.formatted_address)
        });
    });

    document.head.appendChild(script);
}