from .delivery_note import set_naming_series

def before_insert(doc, method):
    set_naming_series(doc)

def set_naming_series(doc):
    naming_series_map = {
        "Real Appliances Private Limited": {
            False: "PR-.YY.-RAPL-.####",
        },
        "Red Star Unit 2": {
            False: "PR-.YY.-RSI-.####",
        }
    }

    if doc.branch in naming_series_map:
        doc.naming_series = naming_series_map[doc.branch][False]