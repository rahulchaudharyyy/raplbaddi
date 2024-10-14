from .stock import execute as stock_fields
from .sales import execute as sales_fields
from .buying import execute as buying_fields

def execute():
    stock_fields()
    sales_fields()
    buying_fields()