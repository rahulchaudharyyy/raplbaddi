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
        const { items } = await frappe.db.get_doc('Paper Name', frm.doc.paper_name);
        const newItemList = items.map(item => ({
            'box': `PB${item.capacity}${item.model.slice(0,1)} ${frm.doc.box_particular}`,
            'paper': `PP ${frm.doc.box_particular} ${frm.doc.paper_name}`,
            'model': item.model,
            'capacity': item.capacity,
            'paper_type': frm.doc.paper_type,
            'paper_name': frm.doc.paper_name
        }));

        const mergedItems = [...frm.doc.items, ...newItemList]
            .filter((item, index, self) =>
                index === self.findIndex(i =>
                    i.model === item.model &&
                    i.capacity === item.capacity &&
                    i.paper_type === item.paper_type &&
                    i.paper_name === item.paper_name
                )
            )
        frm.set_value('items', mergedItems);
        frm.refresh_field('items');
        frm.set_value('paper_name', '')
        frm.set_value('sub_box_type', '')
        frm.set_value('paper_type', '')
    } catch (error) {
        console.error('An error occurred:', error);
    }
}