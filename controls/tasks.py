import frappe
from frappe.utils import nowdate
from frappe import _

def logout_expired_sessions():
    admin_doctype_control = frappe.get_single("Admin Doctype Control")
    expire_date = admin_doctype_control.expire_date
    
    # Proceed to check the expiry date for non-administrator users
    if frappe.session.user != 'Administrator' and expire_date and expire_date <= nowdate():
        # If the expiry date has passed, invalidate the session
        invalidate_session()

def invalidate_session():
    frappe.session['session_expired'] = True
    frappe.msgprint("Your session has expired. Please log in again.")
    frappe.local.login_manager.logout()
    frappe.local.flags.redirect_location = '/login'
    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = "/login"
