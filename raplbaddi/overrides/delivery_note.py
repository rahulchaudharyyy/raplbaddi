import frappe

def before_insert(doc, method):
    set_naming_series(doc)

def set_naming_series(doc):
    naming_series_map = {
        "Real Appliances Private Limited": {
            False: "DN-.YY.-RAPL-.####",
            True: "DRET-.YY.-RAPL-.####"
        },
        "Red Star Unit 2": {
            False: "DN-.YY.-RSI-.####",
            True: "DRET-.YY.-RSI-.####"
        }
    }

    if doc.branch in naming_series_map:
        doc.naming_series = naming_series_map[doc.branch][False]

def validate(doc, method):
    validate_naming_series(doc)

from raplbaddi.utils import make_fields_set_only_once
def validate_naming_series(doc):
    make_fields_set_only_once(doc, ["branch"])