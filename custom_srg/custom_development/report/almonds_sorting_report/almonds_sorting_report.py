# Copyright (c) 2023, SRG and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe.utils import cint, flt

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_filtered_stock_entries(filters)
	return columns, data

def get_columns():
    columns=[
            {
				"label": "Batch No",
				"fieldname": "batch_id",
				"fieldtype": "Link",
				"options": "batch",
				"width": 250,
			},
			{
				"label": "Item Name",
				"fieldname": "item_name",
				"width": 250,
			},
			{
				"label": "QTY",
				"fieldname": "transfer_qty",
				"width": 250,
			},
			{
				"label": "UOM",
				"fieldname": "stock_uom",
				"width": 100,
			},
			{
				"label": "Percent",
				"fieldname": "avg_percent",
				"width": 100,
			},
    ]
    return columns
    
def get_filtered_stock_entries(filters):
	precision = cint(frappe.db.get_single_value("System Settings", "float_precision"))
	stock_entries = frappe.db.get_list("Stock Ledger Entry",filters={"docstatus":1,"batch_no":filters.batch_no},fields={"voucher_no"},pluck="voucher_no")
	average = {}
	for stock_entry in stock_entries:
		items = frappe.db.get_list("Stock Entry",filters={"name":stock_entry,"purpose":"Repack"},fields={"items.item_code","items.item_name","items.transfer_qty","items.stock_uom","items.batch_no"})
		for item in items:
			if item['item_code'] not in average:
				average[item['item_code']] = item
				item['batch_id'] = item.pop("batch_no")
			else:
				average[item['item_code']]["transfer_qty"] += item["transfer_qty"]
			average[item['item_code']]["transfer_qty"] = flt(average[item['item_code']]["transfer_qty"],precision)
	average = list(average.values())
	main = 0
	diff = 0
	for i in range(len(average)):
		if average[i]["item_code"] == filters.item_code:
			main = average[i]["transfer_qty"]
		else:
			diff += average[i]["transfer_qty"]
	average.append(
		{
			'transfer_qty': main-diff,
			'item_name': 'Difference',
			'stock_uom': 'Kg',
			'item_code': 'NA',
			'batch_id': 'NA'
		}
	)
	average = sorted(average, key=lambda d: d['batch_id']) 
	if main != 0:
		for i in range(len(average)):
			average[i]["avg_percent"] = str(flt((average[i]["transfer_qty"]/main)*100,precision))+"%"
	return average
