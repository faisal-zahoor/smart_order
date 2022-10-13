from __future__ import unicode_literals
import frappe
from frappe import msgprint
from frappe.model.document import Document
from frappe.utils import money_in_words

def makeMR(doc,method):
	items = []
	for d in doc.items:
		if d.qty > d.actual_qty and d.qty < d.total_stock:
			mr = frappe.get_doc({
			"doctype": "Material Request",
			"material_request_type": "Material Transfer",
			"schedule_date": doc.transaction_date,
			"transaction_date": doc.transaction_date,
			"against_sales_order":doc.name,
			"items": [{
				"item_code": d.item_code,
				"qty": 1,
				"so_qty": d.qty,
				"warehouse":d.warehouse,
				"sales_order":doc.name
				}]
			})
			mr.insert(ignore_permissions=True)
			mr.save()
			frappe.msgprint("Material Transfer Request Created")

		if d.qty > d.actual_qty and d.qty > d.total_stock:
			mr = frappe.get_doc({
			"doctype": "Material Request",
			"material_request_type": "Material Transfer",
			"schedule_date": doc.transaction_date,
			"transaction_date": doc.transaction_date,
			"against_sales_order":doc.name,
			"items": [{
				"item_code": d.item_code,
				"qty": 1,
				"so_qty": d.qty,
				"warehouse":d.warehouse,
				"sales_order":doc.name
				}]
			})
			mr.insert(ignore_permissions=True)
			mr.save()
			frappe.msgprint("Material Transfer Request Created")

			n_mr = frappe.get_doc({
			"doctype": "Material Request",
			"material_request_type": "Purchase",
			"schedule_date": doc.transaction_date,
			"transaction_date": doc.transaction_date,
			"against_sales_order":doc.name,
			"items": [{
				"item_code": d.item_code,
				"qty": 1,
				"so_qty": d.qty,
				"warehouse":d.warehouse,
				"sales_order":doc.name
				}]
			})
			n_mr.insert(ignore_permissions=True)
			n_mr.save()
			frappe.msgprint("Material Purchase Request Created")

def addBarcode(doc,method):
	if not doc.barcode_status:
		br = frappe.get_doc({
		"doctype" : "Barcode Print",
		"item_code" : doc.item_code,
		"item_name" : doc.item_name,
		"barcode" : doc.barcode,
		"item_price": doc.standard_rate,
		"number_of_copies": 1
		})
		br.insert(ignore_permissions=True)
		br.save()
	else:
		pass

def updateBarcode(doc,method):
	if doc.barcode_status:
		br = frappe.get_doc("Barcode Print",doc.item_code)
		br.barcode = doc.barcode
		br.item_price = doc.standard_rate
		br.save()
	else:
		pass


@frappe.whitelist(allow_guest=True)
def getVAL_Rate(customer):
        val_rate = frappe.db.sql("""select IF(status='Overdue', "1", "0") from `tabSales Invoice` where 
			customer = %s and status = 'overdue' order by creation desc limit 1;;""",(customer))
        return val_rate[0][0] if val_rate else 0.0
