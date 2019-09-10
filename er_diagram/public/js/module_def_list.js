function genErHtml(src){
    let img = "<img src=\"/" + src + "\" target=\"_blank\"/>" ;
    return "<a href=\"/" + src + "\" target=\"_blank\">" + img + "</a>";
}

frappe.listview_settings['Module Def'] = {
    // hide_name_column: true, // hide the last column which shows the `name`
    onload(listview){
        listview.page.add_action_item("Generate Er Diagram", () => {
            frappe.call("er_diagram.utils.getDot", {
                items: listview.get_checked_items()
            }).then(res => {
                if (res.message.status === "sucess"){
                    frappe.msgprint(genErHtml(res.message.data));
                } else if (res.message.status === "failure"){
                    frappe.msgprint("Error during request: " + res.message.data);
                }
                // console.log(res);
                // frappe.msgprint(genErHtml(res.message));
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
    },
};

