import frappe
from frappe.model.document import Document

class PBCreationTool(Document):
    def before_insert(self):
        for i in self.items:
            item_code = f'PB{i.capacity}{i.model[:1]} {self.box_particular}'
            item_paper_code = f'PP {self.box_particular} {i.box_paper_category}'
            item, item_paper = self.get_or_create_item(item_code, item_paper_code, i)
            item.disabled = not i.enabled
            item.save()
            item_paper.save()

    def on_update_after_submit(self):
        for i in self.items:
            item_code = f'PB{i.capacity}{i.model[:1]} {self.box_particular}'
            self.update_item(item_code, i)

    def get_or_create_item(self, item_code, item_paper_code, i):
        try:
            item = frappe.get_doc("Item", item_code)
        except frappe.exceptions.DoesNotExistError:
            item = self.create_item(item_code, i)

        try:
            item_paper = frappe.get_doc("Item", item_paper_code)
        except frappe.exceptions.DoesNotExistError:
            item_paper = self.create_item(item_paper_code, i)

        i.item = item.name
        i.item_paper = item_paper.name
        return item, item_paper

    def create_item(self, item_code, i):
        item = frappe.new_doc("Item")
        item.item_code = item_code
        item.item_name = item_code
        item.name = item_code
        item.description = item_code
        item.item_group = 'Packing Boxes' if item_code.startswith('PB') else 'Packing Paper'
        item.geyser_model = i.model
        item.capacity = i.capacity
        item.stock_uom = 'Nos' if item.item_group == 'Packing Boxes' else 'Set 2'
        item.is_stock_item = 1
        item.append("item_defaults", {"default_warehouse": 'Packing Boxes - Rapl', "company": 'Real Appliances Private Limited'})
        if self.box_type == 'Brand':
            item.brand = self.box_particular
        else:
            item.plain_box_type = self.box_particular
        item.save()
        return item

    def update_item(self, item_code, i):
        try:
            item = frappe.get_doc("Item", item_code)
            item.disabled = not i.enabled
            item.geyser_model = i.model
            item.capacity = i.capacity
            item.save()
        except frappe.exceptions.DoesNotExistError:
            pass