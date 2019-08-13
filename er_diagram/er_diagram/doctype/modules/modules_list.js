frappe.listview_settings['Modules'] = {
    hide_name_column: true, // hide the last column which shows the `name`
    onload(listview) {
        listview.page.add_action_icon(
            __("fa fa-upload import-action"),
            function(){
                $(".import-action").removeClass("fa-upload").addClass("fa-spinner fa-pulse");
                frappe.db.get_list("Module Def", {
                    fields: ['name'],
                    filters: {}
                }).then(modules => {
                    console.log("getting dules");
                    console.log(modules);
                    modules.map(mod =>  {
                        console.log("inserting: " +mod);
                        frappe.call({
                            method: 'er_diagram.utils.setDocument',
                            args: {
                                docDict: {
                                    docType: "Modules",
                                    module_name: mod.name,
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
                    });
                });
            });
    },
};
