
function genErHtml(src){
    let img = "<img src=\"/" + src + "\" target=\"_blank\"/>" ;
    return "<a href=\"/" + src + "\" target=\"_blank\">" + img + "</a>";
}

frappe.listview_settings['Installed Modules'] = {
    hide_name_column: true, // hide the last column which shows the `name`
    onload(listview){
        listview.page.add_action_item("Generate Er Diagram", () => {
            frappe.call("er_diagram.utils.getDot", {
                items: listview.get_checked_items()
            }).then(res => {
                console.log(res);
                frappe.msgprint(genErHtml(res.message));
            });

        });

        listview.page.add_action_item("Generate Er Diagram with Datafields", () => {
            frappe.call("er_diagram.utils.getDot", {
                items: listview.get_checked_items(),
                addFields: "True"
            }).then(res => {
                console.log(res);
                frappe.msgprint(genErHtml(res.message));
            });

        });
    },
    refresh(listview) {
        frappe.db.get_list("Module Def", {
            fields: ['name'],
            filters: {}
        }).then(modules => {
            frappe.db.get_list("Installed Modules").then(installed => {
                modules.filter(mod => {
                    return !(installed.map(x => x.name).includes(mod.name));
                }).map(mod =>  {
                    frappe.db.insert({
                        doctype: 'Installed Modules',
                        module_link: mod.name
                    });
                });
            });
        });
    },
};




/*
frappe.call({
    method: 'er_diagram.utils.setDocument',
    args: {
        docDict: {
            "doctype": "Installed Modules",
            "module_name": mod.name
        },
        name: mod.name
    },
    // freeze the screen until the request is completed
    freeze: false,

    callback: (r) => {
        listview.refresh();
    },
    error: (r) => {
        frappe.msgprint("import failure: " + r);
        $(".import-action").removeClass("fa-spinner fa-pulse").addClass("fa-upload");
        listview.refresh();
    }
});
*/
