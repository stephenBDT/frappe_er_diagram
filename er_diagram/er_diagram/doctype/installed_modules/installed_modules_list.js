
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
        frappe.call("er_diagram.er_diagram.api.update_installed_modules");
    },
};

