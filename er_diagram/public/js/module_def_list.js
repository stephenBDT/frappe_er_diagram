function genErHtml(src){
    let img = "<img src=\"/" + src + "\" target=\"_blank\"/>" ;
    return "<a href=\"/" + src + "\" target=\"_blank\">" + img + "</a>";
}

function genGraphMLHtml(src){
    let img = "<i class='fa fa-download' aria-hidden='true'></i>";
    let span = '<span>Click the download button, save and open the file in yEd. <br>Select all (ctrl + a), go to Tools -> Fit Node to Label.<br>Ensure all checkboxes are unchecked, click ok. <br>Then you may want to got Layout and select a layout you like. Enjoy!</span>';
    return span + "<br>" + "<a style='font-size:36px' href=\"" + src + "\" target=\"_blank\">" + img + "</a>";
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
                debugger;
                console.log(res);
                frappe.msgprint(genErHtml(res.message.data));
            });

        });
        listview.page.add_action_item("Generate graphml file for Er Diagram", () => {
            frappe.call("er_diagram.utils.getDot", {
                items: listview.get_checked_items(),
                graphML: "True"
            }).then(res => {
                console.log(res);
                frappe.msgprint(genGraphMLHtml(res.message.data));
            });

        });
        listview.page.add_action_item("Generate graphml file for Er Diagram with Datafields", () => {
            frappe.call("er_diagram.utils.getDot", {
                items: listview.get_checked_items(),
                graphML: "True",
                addFields: "True"
            }).then(res => {
                console.log(res);
                frappe.msgprint(genGraphMLHtml(res.message.data));
            });

        });
    },
    refresh(listview) {
    },
};

