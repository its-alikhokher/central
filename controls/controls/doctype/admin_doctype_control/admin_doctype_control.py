# Copyright (c) 2024, Nextash and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.utils import getdate
from frappe.model.document import Document
from frappe import _
from frappe.query_builder import Order
from frappe.sessions import delete_session

class AdminDoctypeControl(Document):
    def validate(self):
        if not frappe.session.user == "Administrator":
            frappe.throw(_("Not Allowed to Update"))
        self.validate_expiry()

    def validate_expiry(self):
        if getdate(self.expire_date) < getdate():
            self.clear_sessions()

    def clear_sessions(self):
        session = frappe.qb.DocType("Sessions")
        session_id = frappe.qb.from_(session).where(session.user != "Administrator")

        query = (
            session_id.select(session.sid).orderby(session.lastupdate, order=Order.desc)
        )

        sessions = query.run(pluck=True)
        for d in sessions:
            delete_session(d, reason="Subscription Expired")
    
