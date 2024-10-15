from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

custom_fields = {
    "Sales Order": [
        {
            "is_system_generated": 1,
            "label": "Dispatch Remarks",
            "fieldname": "dispatch_remarks",
            "insert_after": "planning_remarks",
            "fieldtype": "Data",
            "depends_on": 'eval:frappe.session.user == "kumarom906@gmail.com" ||\n    frappe.session.user == "Administrator" || \n    frappe.session.user == "iamcasg@gmail.com" ||\n    frappe.session.user == "abhishek.rapl417@gmail.com"',
            "read_only": 0,
            "hidden": 0,
            "no_copy": 0,
            "allow_on_submit": 1,
        },
        {
            "is_system_generated": 1,
            "label": "Bill To Ship To",
            "fieldname": "is_bill_to_ship_to",
            "insert_after": "no_delivery_date",
            "fieldtype": "Check",
            "read_only": 0,
            "hidden": 0,
            "no_copy": 0,
            "reqd": 0,
            "allow_on_submit": 0,
        },
    ],
    "Sales Order Item": [
        {
            "is_system_generated": 1,
            "label": "Color",
            "fieldname": "color",
            "insert_after": "delivery_date",
            "fieldtype": "Link",
            "default": "Regular",
            "options": "Color",
            "reqd": 0,
            "allow_on_submit": 1,
            "in_list_view": 1,
            "columns": 1,
            "reqd": 1,
        }
    ],
    "Delivery Note": [
        {
            "is_system_generated": 1,
            "label": "Branch",
            "fieldname": "branch",
            "insert_after": "company",
            "fieldtype": "Link",
            "default": "Real Appliances Private Limited",
            "options": "Branch",
            "reqd": 1,
            "allow_on_submit": 0,
        },
        {
            "is_system_generated": 1,
            "label": "Driver Number",
            "fieldname": "driver_number",
            "insert_after": "lr_date",
            "fieldtype": "Data",
            "reqd": 1,
            "allow_on_submit": 0,
        },
        {
            "is_system_generated": 1,
            "label": "Bilty/LR No,",
            "fieldname": "bilty_no",
            "insert_after": "driver_number",
            "fieldtype": "Data",
            "reqd": 1,
            "allow_on_submit": 0,
        },
        {
            "is_system_generated": 1,
            "label": "Internal Receipt",
            "fieldname": "internal_receipt",
            "insert_after": "is_return",
            "fieldtype": "Link",
            "options": "Stock Entry",
            "is_hidden": 1,
            "read_only": 1,
            "no_copy": 1,
            "reqd": 0,
            "allow_on_submit": 1,
        },
        {
            "is_system_generated": 1,
            "label": "Freight Status",
            "fieldname": "freight_status",
            "insert_after": "amount",
            "fieldtype": "Select",
            "default": "Already Paid by us",
            "options": "Already Paid by us\nPlease pay to Driver",
            "reqd": 1,
            "allow_on_submit": 0,
        },
    ],
}


def execute():
    create_custom_fields(custom_fields)


property_setters = [
    {
        "doctype": "Property Setter",
        "name": "Sales Order-customer_group-hidden",
        "is_system_generated": 0,
        "doctype_or_field": "DocField",
        "module": "Raplbaddi",
        "doc_type": "Sales Order",
        "field_name": "customer_group",
        "property": "hidden",
        "property_type": "Int",
        "value": 0,
    },
    {
        "name": "Sales Order-main-field_order",
        "is_system_generated": 0,
        "doctype_or_field": "DocType",
        "doc_type": "Sales Order",
        "property": "field_order",
        "property_type": "Data",
        "value": '["remote_site_name", "remote_docname", "approval", "audit", "planning_remarks", "dispatch_remarks", "customer_section", "column_break0", "title", "naming_series", "customer", "customer_name", "tax_id", "order_type", "column_break_7", "transaction_date", "customer_group", "delivery_dates", "mark", "custom_status", "delivery_date_expected_by_customer", "no_delivery_date", "is_bill_to_ship_to", "column_break_ks7gm", "submission_date", "delivery_date", "sample", "column_break1", "po_no", "discount_in_rs", "update_discount", "remove_discount", "apply_old_discounts", "po_date", "sales_person", "column_break_zozud", "so_number", "company", "skip_delivery_note", "is_reverse_charge", "is_export_with_gst", "amended_from", "section_conditions", "conditions", "section_break_rn4ow", "billing_rule", "column_break_b4bwc", "shipping_rule_rapl", "accounting_dimensions_section", "cost_center", "dimension_col_break", "project", "currency_and_price_list", "currency", "conversion_rate", "column_break2", "selling_price_list", "price_list_currency", "plc_conversion_rate", "ignore_pricing_rule", "sec_warehouse", "scan_barcode", "column_break_28", "set_warehouse", "reserve_stock", "items_section", "items", "section_break_31", "total_qty", "total_net_weight", "column_break_33", "base_total", "base_net_total", "column_break_33a", "total", "net_total", "taxes_section", "tax_category", "taxes_and_charges", "column_break_38", "shipping_rule", "column_break_49", "incoterm", "named_place", "section_break_40", "taxes", "section_break_43", "base_total_taxes_and_charges", "column_break_46", "total_taxes_and_charges", "totals", "base_grand_total", "base_rounding_adjustment", "base_rounded_total", "base_in_words", "column_break3", "grand_total", "rounding_adjustment", "rounded_total", "in_words", "advance_paid", "disable_rounded_total", "section_break_48", "apply_discount_on", "base_discount_amount", "coupon_code", "column_break_50", "additional_discount_percentage", "discount_amount", "sec_tax_breakup", "other_charges_calculation", "section_gst_breakup", "gst_breakup_table", "packing_list", "packed_items", "pricing_rule_details", "pricing_rules", "contact_info", "billing_address_column", "customer_address", "address_display", "billing_address_gstin", "gst_category", "place_of_supply", "territory", "column_break_84", "contact_person", "contact_display", "contact_phone", "contact_mobile", "contact_email", "shipping_address_column", "shipping_address_name", "shipping_address", "column_break_93", "dispatch_address_name", "dispatch_address", "col_break46", "company_address", "company_gstin", "column_break_92", "company_address_display", "payment_schedule_section", "payment_terms_section", "payment_terms_template", "payment_schedule", "terms_section_break", "tc_name", "terms", "more_info", "section_break_78", "status", "delivery_status", "per_delivered", "column_break_81", "per_billed", "per_picked", "billing_status", "sales_team_section_break", "sales_partner", "column_break7", "amount_eligible_for_commission", "commission_rate", "total_commission", "section_break1", "sales_team", "loyalty_points_redemption", "loyalty_points", "column_break_116", "loyalty_amount", "subscription_section", "from_date", "to_date", "column_break_108", "auto_repeat", "update_auto_repeat_reference", "printing_details", "letter_head", "group_same_items", "column_break4", "select_print_heading", "language", "additional_info_section", "is_internal_customer", "represents_company", "column_break_152", "source", "inter_company_order_reference", "campaign", "party_account_currency", "connections_tab", "term", "terms_and_shipping_rule", "boxes", "fetch_boxes", "sale_order_item_boxes", "owner_no_first", "ecommerce_gstin", "ecommerce_supply_type", "gst_col_break"]',
        "doctype": "Property Setter",
    },
]
