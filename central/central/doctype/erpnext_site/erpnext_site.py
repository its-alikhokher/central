import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate
from frappe.frappeclient import FrappeClient


class ERPNextSite(Document):
    def validate(self):
        self.update_expiry()
        if self.update_on_save:
            self.update_customer_site()

    def update_expiry(self):
        self.status = "Active"
        if getdate(self.subscription_expiry) < getdate():
            self.status = "Expired"

    @frappe.whitelist()
    def load_package(self):
        if not self.package:
            return
        package = frappe.get_doc("ERPNext Packages", self.package)
        self.limits = []
        for d in package.limits:
            self.append(
                "limits", {"doctype_list": d.doctype_list, "limit": d.limit})
        self.currency = package.currency
        self.monthly_price = package.monthly_price
        self.yearly_price = package.yearly_price

    def get_site_url(self):
        url = "https://{0}".format(self.name)
        if self.protocol == "Http":
            url = "http://{0}".format(self.name)
        return url

    @frappe.whitelist()
    def update_customer_site(self):
        client = FrappeClient(self.get_site_url())
        try:
            client._login(username="Administrator",
                          password=self.get_password("password"))
        except Exception as e:
            frappe.throw(_("Login Failed. Please check Password and Site URL"))

        doc = frappe._dict()
        doc.doctype = "Admin Doctype Control"
        doc.name = "Admin Doctype Control"
        doc.expire_date = self.subscription_expiry
        doc.doctype_list_table = []
        for d in self.limits:
            doc.doctype_list_table.append(
                {"doctype_list": d.doctype_list, "limit": d.limit})

        client.update(doc)
        frappe.msgprint(msg="Site Updated Successfully.", indicator="green")


@frappe.whitelist()
def update_doctype_on_site(site, doctype_name):
    site_doc = frappe.get_doc("ERPNext Site", site)
    client = FrappeClient(site_doc.get_site_url())
    try:
        client._login(username="Administrator",
                      password=site_doc.get_password("password"))
    except Exception as e:
        frappe.throw(_("Login Failed. Please check Password and Site URL"))

    def update_customization(client, doc):
        del doc["owner"]
        del doc["creation"]
        del doc["modified"]
        del doc["modified_by"]
        doc["doctype"] = "Custom Field"
        if "doc_type" in doc:
            doc["doctype"] = "Property Setter"


        if doc["doctype"] == "Custom Field" and doc["fieldtype"] in ["Table", "Link"]:
            custom_doc = frappe.get_doc("DocType", doc["options"]).as_dict()
            if custom_doc.custom == 1:
                del custom_doc["owner"]
                del custom_doc["creation"]
                del custom_doc["modified"]
                del custom_doc["modified_by"]

                try:
                    client.get_doc("DocType", custom_doc["name"])
                    client.update(custom_doc)
                except Exception as e:
                    try:
                        client.insert(custom_doc)
                    except Exception as e:
                        pass

        try:
            client.get_doc(doc["doctype"], doc["name"])
            client.update(doc)
        except Exception as e:
            try:
                client.insert(doc)
            except Exception as e:
                pass




    def sync_customization(client, doctype):
        doctypes = []
        doctypes.extend(frappe.get_all("Custom Field", fields="*", filters={"dt": doctype}))
        doctypes.extend(frappe.get_all("Property Setter", fields="*", filters={"doc_type": doctype}))

        for d in doctypes:
            update_customization(client, d)

    sync_customization(client, doctype_name)

    for d in frappe.get_meta(doctype_name).get_table_fields():
        sync_customization(client, d.options)


@frappe.whitelist()
def update_workspace_on_site(site, workspace):
    site_doc = frappe.get_doc("ERPNext Site", site)
    client = FrappeClient(site_doc.get_site_url())
    try:
        client._login(username="Administrator",
                      password=site_doc.get_password("password"))
    except Exception as e:
        frappe.throw(_("Login Failed. Please check Password and Site URL"))

    workspace_doc = frappe.get_doc("Workspace", workspace).as_dict()
    del workspace_doc["owner"]
    del workspace_doc["creation"]
    del workspace_doc["modified"]
    del workspace_doc["modified_by"]
    workspace_doc["doctype"] = "Workspace"
    try:
        client.get_doc("Workspace", workspace_doc["name"])
        client.update(workspace_doc)
    except Exception as e:
        try:
            client.insert(workspace_doc)
        except Exception as e:
            pass


def update_expiry_of_site():
    expired = frappe.get_all("ERPNext Site", filters={"subscription_expiry": [
                             "<", getdate()], "status": "Active"})
    for d in expired:
        doc = frappe.get_doc("ERPNext Site", d.name)
        doc.update_on_save = 1
        doc.save()
