frappe.ui.form.on('Admin Doctype Control', {
    // validate: function (frm) {
    //     var selected_doctypes = [];
    //     frm.doc.doctype_list_table.forEach(function (row) {
    //         if (row.doctype_list) {
    //             if (selected_doctypes.includes(row.doctype_list)) {
    //                 frappe.msgprint(__("Doctype '{0}' is already selected.", [row.doctype_list]));
    //                 frappe.validated = false;
    //                 return false;
    //             } else {
    //                 selected_doctypes.push(row.doctype_list);
    //             }
    //         }
    //     });
    // }
});

frappe.ui.form.on('Doctype List Table', {
    doctype_list: function (frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        var selectedDocType = child.doctype_list;

       
        var duplicateExists = false;
        frm.doc.doctype_list_table.forEach(function (row) {
            if (row.name !== cdn && row.doctype_list === selectedDocType) {
                duplicateExists = true;
                return false;
            }
        });

        if (duplicateExists) {
            frappe.msgprint("Document type cannot be repeated.");
            cur_frm.fields_dict[cdt].grid.get_field('doctype_list').set_value('');
        }
    }
});
