from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
      {
        "label":_("Er Diagram"),
        "icon": "octicon octicon-briefcase",
          "items": [
              {
                  "type": "doctype",
                  "name": "Installed Modules",
                  "label": _("Installed Modules"),
                  "description": _("Show all the Modules that are currently installed"),
              },
          ]
      }
    ]


