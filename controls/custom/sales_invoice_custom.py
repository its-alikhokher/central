import frappe

def validate_limit(doc, method, target_doctype):
    admin_controls = frappe.get_single("Admin Doctype Control")
    if admin_controls and admin_controls.get("doctype_list_table"):
        doctype_list = admin_controls.get("doctype_list_table")
        target_doctype_limit = None
        for row in doctype_list:
            if row.doctype_list == target_doctype:
                target_doctype_limit = row.limit
                break

        if target_doctype_limit is not None:
            existing_docs_count = frappe.db.count(target_doctype)
            if existing_docs_count >= target_doctype_limit:
                frappe.throw(f"{target_doctype} limit exceeded. Cannot save.")

def on_validate(doc, method):
    validate_limit(doc, method, doc.doctype)
