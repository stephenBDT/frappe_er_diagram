## Er Diagram

Generate ER-Diagrams for [frappe.io](https://frappe.io) DocTypes
This Frappe-App will call a binary that will generate a graphviz .dot file that describes the Graph, representing you Er-Diagram.
Then it will use the 'dot' binary from graphviz to generate a picture from the graph description (the .dot file), which you can display
in your frappe webview.


### How to install:
The easiest way to install the frappe app using the following bench command:
```
bench get-app https://github.com/stephenBDT/frappe_er_diagram.git
bench --site [YOUR SITENAME] install-app er_diagram
```

#### Installing the dependencies
It is important, that you have the haskell binary that actually generates the the Graphdescription
The compiled binary is already included in this repo, but if you don't trust it, please feel free to compile it yourself following this instruction:

If you do trust the binary, all you need to ensure, is that you have graphviz installed and it's binarys in you `PATH` on the system where your frappe instance is running.
In debian/ubuntu you can install it using `sudo apt-get install graphviz`

### How to use:
After installing the er_diagram app into your frappe site, you will see an er_diagram selection on your Frappe Desk. Just click it and contiunue towards 'installed modules' which will forward you to the list view of Frapps' 'Module Def' DocType. Select all the modules for whose DocTypes you want to see the Er-Diagram, click Action and generate the ER-Diagram.
If all goes well you should get a pop-up where you can click the .png image file to see you ER-Diagram in Full Screen. 
Thats It! Enjoy!

#### License
MIT
