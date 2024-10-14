from .delivery_note import set_naming_series

def before_insert(doc, method):
    set_naming_series(doc)