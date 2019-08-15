import frappe


@frappe.whitelist()
def update_installed_modules():

    def insert_if_not_existing(module, target):
        if not frappe.db.exists(target, module['name']):
            doc = frappe.new_doc(target);
            doc.module_link = module['name']
            doc.insert()
            frappe.db.commit()
        else:
            print("document {} already exists".format(module['name']))

    list(map(lambda mod: insert_if_not_existing(mod, "Installed Modules"),
             frappe.db.get_list("Module Def")))

