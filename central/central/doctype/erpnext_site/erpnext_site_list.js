frappe.listview_settings["ERPNext Site"] = {
	get_indicator: function (doc) {
		const status_colors = {
			"Expired": "red",
			"Active": "green"
		};
		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	}
};