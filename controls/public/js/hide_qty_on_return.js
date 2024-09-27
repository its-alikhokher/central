frappe.ui.form.on(cur_frm.doc.doctype, {
	setup: function(frm){
		frm.fields_dict.items
	},
	refresh: function(frm){
		if(frm.is_new() && frm.doc.is_return){
			$.each(frm.doc.items || [], function(i,v){
				if(!v.return_qty){
					frappe.model.set_value(v.doctype, v.name, "return_qty", Math.abs(v.qty));
				}
			});
		}

		frm.fields_dict.items.grid.toggle_display("qty", frm.doc.is_return ? 0 : 1);
		frm.fields_dict.items.grid.toggle_display("return_qty", frm.doc.is_return ? 1 : 0);
		frm.fields_dict.items.grid.reset_grid();
	}
});

frappe.ui.form.on(cur_frm.doc.doctype+" Item", {
	return_qty: function(frm, cdt, cdn){
		var doc = locals[cdt][cdn];
		var qty = 0;
		if (doc.return_qty){
			qty = -1 * doc.return_qty;
		}
		frappe.model.set_value(cdt, cdn, "qty", qty);
	}
});