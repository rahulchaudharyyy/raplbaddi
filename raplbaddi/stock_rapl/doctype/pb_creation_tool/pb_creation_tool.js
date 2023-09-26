// Copyright (c) 2023, Nishant Bhickta and contributors
// For license information, please see license.txt

frappe.ui.form.on('PB Creation Tool', {
    onload(frm) {
        frm.set_query('box_type', () => {
            return {
                filters: [
                    ['name', 'in', ['Brand', 'Plain Box Type']]
                ]
            };
        });
    },

	create_box(frm) {
		create_box(frm)
	  }	  
});

async function create_box(frm) {
    try {
        const { items } = await frappe.db.get_doc('Box Paper Type', frm.doc.box_paper_category);
        const newItemList = items.map(item => ({
            'model': item.model,
            'capacity': item.capacity,
			'box_paper_type': frm.doc.box_paper_type,
			'box_paper_category': frm.doc.box_paper_category
        }));

        const mergedItems = [...frm.doc.items, ...newItemList]
		.filter((item, index, self) =>
		index === self.findIndex(i =>
			i.model === item.model &&
			i.capacity === item.capacity &&
			i.box_paper_type === item.box_paper_type &&
			i.box_paper_category === item.box_paper_category
		)
		)
        frm.set_value('items', mergedItems);
        frm.refresh_field('items');
    } catch (error) {
        console.error('An error occurred:', error);
    }
}