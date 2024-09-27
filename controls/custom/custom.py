import frappe

@frappe.whitelist()
def get_items_with_prices():
    items_with_prices = []
    # Fetch all items from the Item doctype
    items = frappe.get_all("Item", fields=["name", "item_name", "description"])
    # Iterate through each item
    for item in items:
        # Get the selling price of the item
        price = frappe.db.get_value("Item Price", {"item_code": item.name}, "price_list_rate")
        # Get the UOM from the first Item Prize entry (if exists)
        uom = frappe.db.get_value("Item Price", {"item_code": item.name}, ["uom"], order_by="idx")
        items_with_prices.append({
            "item_code": item.name,
            "item_name": item.item_name,
            "description": item.description,
            "price": price if price else 0.0,
            "uom": uom
        })
    return items_with_prices
