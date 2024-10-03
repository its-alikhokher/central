frappe.ui.form.on("ERPNext Site", {
	refresh: function (frm) {
		frm.set_query("doctype_list", "limits", function () {
			return {
				filters: {
					issingle: 0,
					istable: 0
				}
			}
		});
		frm.add_custom_button(__("Update Customer Site"), function () {
			frm.trigger("update_customer_site");
		}).addClass("btn-primary");

		frm.add_custom_button(__("Update Workspace"), function () {
			frm.trigger("update_workspace");
		})

		// Add custom button for Update Doctype
		frm.add_custom_button(__("Update Customization"), function () {
			let d = new frappe.ui.Dialog({
				title: __("Update Doctype"),
				fields: [
					{
						label: __("Doctype Name"),
						fieldname: "doctype_name",
						fieldtype: "Link",
						options: "DocType",
						reqd: 1
					}
				],
				primary_action_label: __("Update"),
				primary_action(values) {
					frm.call({
						method: "update_doctype_on_site",
						args: {
							site: frm.doc.name,
							doctype_name: values.doctype_name
						},
						freeze: true,
						freeze_message: "Custimizaton is being updated...",
						callback: function (r) {
							frappe.msgprint({
									title: __('Notification'),
									indicator: 'green',
									message: __('Customization updated successfully on the customer site.')
								});
							d.hide();
						}
					});
				}
			});
			d.show();
		}).addClass("btn-primary");
	},
	package: function (frm) {
		frm.call({
			method: "load_package",
			doc: frm.doc,
			freeze: true,
			freeze_message: __("Loading Package"),
			callback: function (r) {
				frm.refresh_fields();
			}
		});
	},
	update_workspace: function(frm){
		let d = new frappe.ui.Dialog({
				title: __("Update Workspace"),
				fields: [
					{
						label: __("Workspace Name"),
						fieldname: "workspace",
						fieldtype: "Link",
						options: "Workspace",
						reqd: 1
					}
				],
				primary_action_label: __("Update"),
				primary_action(values) {
					frm.call({
						method: "update_workspace_on_site",
						args: {
							site: frm.doc.name,
							workspace: values.workspace
						},
						freeze: true,
						freeze_message: "Workspace is being updated...",
						callback: function (r) {
							frappe.msgprint({
									title: __('Notification'),
									indicator: 'green',
									message: __('Workspace updated successfully on the customer site.')
								});
							d.hide();
						}
					});
				}
			});
			d.show();
	},
	update_customer_site: function (frm) {
		frm.call({
			method: "update_customer_site",
			doc: frm.doc,
			freeze: true,
			freeze_message: __("Updating Customer Site"),
			callback: function (r) {
				frappe.msgprint({
					title: __('Notification'),
					indicator: 'green',
					message: __('Customer site updated successfully.')
				});
			}
		});
	}
});
