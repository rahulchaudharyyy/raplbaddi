import frappe
from frappe.model.document import Document

class PBCreationTool(Document):
    def get_item_code(self, item, item_type):
        item_code_formats = {
            "Box": f'PB{item.capacity}{item.model[:1]} {self.box_particular}',
            "Paper": f'PP {self.box_particular} {item.paper_name}',
        }
        
        return item_code_formats.get(item_type)
    
    def get_total_safety_stock(self, i):
        for item in self.items:
            safety_stock_list = [item.safety_stock for item in self.items if i.paper_name == item.paper_name]
        return sum(safety_stock_list)
                
    
    def validate(self):
        for item in self.items:
            try:
                box_code = self.get_item_code(item, item_type='Box')
                box = frappe.get_doc("Item", box_code)
                item.box = box.name
            except frappe.exceptions.DoesNotExistError:
                item.box = ''

            try:
                paper_code = self.get_item_code(item, item_type='Paper')
                paper = frappe.get_doc("Item", paper_code)
                item.paper = paper.paper
            except frappe.exceptions.DoesNotExistError:
                item.paper = ''
   
    def before_submit(self):
        for item in self.items:
            box_code, paper_code = self.get_item_code(item, item_type='Box'), self.get_item_code(item, item_type='Paper')
            box, paper = self.get_or_create_item(box_code, paper_code, item, self.get_total_safety_stock(item))
            if not item.box_enabled:
                box.disabled = True
            box.save(), paper.save()

    
    def on_update_after_submit(self):
        for item in self.items:
            box_code, paper_code = self.get_item_code(item, item_type='Box'), self.get_item_code(item, item_type='Paper')
            enable_paper = False if len([item.box_enabled for item in self.items if item.box_enabled]) == 0 else True
            box, paper = self.get_or_create_item(box_code, paper_code, item, self.get_total_safety_stock(item))
            if not item.box_enabled:
                box.disabled = True
            paper.disabled = not enable_paper
            
            box.save(), paper.save()

    def get_or_create_item(self, box_code, paper_code, item, total_safety_stock):
        try:
            box = frappe.get_doc("Item", box_code)
        except frappe.exceptions.DoesNotExistError:
            box = self.create_item(box_code, item)

        try:
            paper = frappe.get_doc("Item", paper_code)
        except frappe.exceptions.DoesNotExistError:
            paper = self.create_item(paper_code, item)

        item.box = box.name
        item.paper = paper.name
        box.disabled = not item.box_enabled
        box.safety_stock = item.safety_stock if box.safety_stock == 0 else box.safety_stock
        paper.safety_stock = total_safety_stock
        return box, paper

    def create_item(self, box_code, i):
        item = frappe.new_doc("Item")
        item.item_code = box_code
        item.item_name = box_code
        item.name = box_code
        item.description = box_code
        item.item_group = 'Packing Boxes' if box_code.startswith('PB') else 'Packing Paper'
        item.geyser_model = i.model
        item.capacity = i.capacity,
        item.safety_stock = i.safety_stock if item.item_group == 'Packing Boxes' else i.safety_stock * (i.paper_name.count('-') + 1)
        item.stock_uom = 'Nos' if item.item_group == 'Packing Boxes' else 'Set 2'
        item.is_stock_item = 1
        item.append("item_defaults", {"default_warehouse": 'Packing Boxes - Rapl', "company": 'Real Appliances Private Limited'})
        if self.box_type == 'Brand':
            item.brand = self.box_particular
        else:
            item.plain_box_type = self.box_particular
        item.save()
        return item