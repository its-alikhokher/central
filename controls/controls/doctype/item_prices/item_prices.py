# Copyright (c) 2024, Nextash and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ItemPrices(Document):
	pass



@frappe.whitelist()
def get_item_prices(item_code, invoice_type):
	item = frappe.get_doc("Item", item_code)
	if item.prices_enabled:
		return {"prices": frappe.get_all("Item Prices", filters={"parent": item_code, "type": invoice_type}, fields=["*"]), "enabled": True}

	return {"prices": [], "enabled": False}