import { createApp } from "vue";
import App from "./App.vue";
import VueGoogleMaps from '@fawmi/vue-google-maps';

class Crp {
	constructor({ page, wrapper }) {
		this.$wrapper = $(wrapper);
		this.page = page;

		this.init();
	}

	init() {
		this.setup_page_actions();
		this.setup_app();
	}

	setup_page_actions() {
		this.primary_btn = this.page.set_primary_action(__("Print Message"), () =>
			frappe.msgprint("Hello My Page!")
			);
		this.page.clear_primary_action()
		this.btn = this.page.set_secondary_action('RF', () => refresh(), 'octicon octicon-sync')
		this.page.add_menu_item('Send Email', () => open_email_dialog())
		this.page.add_menu_item('Send', () => open_email_dialog(), true)
		this.page.add_action_item('Delete', () => this.delete_items())
	}
	delete_items() {
		console.log("This")
		this.page.add_inner_button('New Post', () => new_post(), 'Make')
		this.page.change_inner_button_type('Delete Posts', 'Actions', 'danger');
	}

	setup_app() {
		// create a vue instance
		let app = createApp(App);
		// mount the app
		this.$crp = app.use(VueGoogleMaps, {
			load: {
			  key: 'AIzaSyCkSq_Cl0y1rExRjwHL6z-10P03D5MbOLc',
			  libraries: 'places',
			},
		  }).mount(this.$wrapper.get(0));
	}
}

frappe.provide("frappe.ui");
frappe.ui.Crp = Crp;
export default Crp;