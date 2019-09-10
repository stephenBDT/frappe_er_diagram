import subprocess
import frappe
import json
from collections import namedtuple
# -*- coding: utf-8 -*-

def debug(s):
    frappe.logger().debug(s)


@frappe.whitelist()
def getDot(items, addFields=False):

    # TODO UGLY!! No need for two flags!
    addFieldsFlag = "-l" if addFields else "-f"

    modules = json.loads(items)
    print ("-------------------------------------")
    print (modules)
    # modules = list(map(lambda mod: namedtuple("Modules", mod.keys())(*mod.values()), modules))
    def runCmd(cmdArr):
        print ("running with")
        print (cmdArr)
        return subprocess.run(cmdArr, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def getItemInfo(mod):
        print(mod)
        app_name = mod['app_name'].replace(" ", "_").lower()
        module_name = mod['module_name'].replace(" ", "_").lower()
        outFileName = app_name + module_name + addFieldsFlag
        docTypePath = "../apps/" + app_name + "/" +app_name + "/" + module_name + "/"
        return (docTypePath, outFileName)

    relevantItemInformation = list(map(getItemInfo, modules))
    docTypeFilePaths = list(map(lambda a: a[0], relevantItemInformation))
    outFileName = "".join(list(map(lambda a:a[1], relevantItemInformation)))
    outPath = "../apps/er_diagram/er_diagram/www/pngs/" + outFileName + ".png"

    # TODO UGLY!! No need for two flags!
    addFieldsFlag = "-l" if addFields else "-f"

    completedDotGeneration = runCmd(["../apps/er_diagram/frappe-er-exe", addFieldsFlag, "-o" + outFileName] + docTypeFilePaths)
    if completedDotGeneration.returncode == 0:
        try:
            completedPngGeneration = runCmd(["dot", "-Tpng", "-o" + outPath, outFileName])
            if completedPngGeneration.returncode == 0:
                return {"status": "sucess", "data": "pngs/" + outFileName + ".png"}
            else:
                return {"status": "failure", "data": "Crashed in Png Generation: " + completedPngGeneration.stderr}
        except Exception as e:
            return {"status": "failure", "data": "Please make sure you have graphvizs' dot application instaslled on your server"}
    else:
        return "Crashed in Dot Generation: " + completedDotGeneration.stderr



@frappe.whitelist()
def run(app_name, module_name, optional = None ):

    if optional is not None:
        list(map(lambda t: print(t), json.loads(optional)))
    app_name = app_name.replace(" ", "_").lower()
    module_name = module_name.replace(" ", "_").lower()

    target = "../apps/" + app_name + "/" +app_name + "/" + module_name + "/"
    outFileName = app_name + module_name
    outPath = "../apps/er_diagram/er_diagram/www/" + outFileName + ".png"
    # This always executes in bench/sites/
    debug("generating er for: " + target.lower())

    import tempfile
    with tempfile.TemporaryFile() as dotFile:
        completedDotGeneration = subprocess.run(["../apps/er_diagram/frappe-er-exe", "-o" + dotFile, target.lower()], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if completedDotGeneration.returncode == 0:
            completedPngGeneration = subprocess.run(["dot", "-Tpng", "-o" + outPath, dotFile], universal_newlines=True, stdout=subprocess.PIPE)
            if completedPngGeneration.returncode == 0:
                return outFileName + ".png"
            else:
                return "Crashed in Png Generation"
        else:
            return "Crashed in Dot Generation: " + completedDotGeneration.stderr

@frappe.whitelist()
def hello(names):
    frappe.msgprint(names);



@frappe.whitelist()
def setDocument(docDict, metadata={}, name = None):
    "This is a not so nice way, but consisten way of inserting/updating\
    a DocType that supports genName(). It allows for the name generation\
    to be only ever in genName() and nowhere else"
    doc = frappe.get_doc(docDict) # create an in memory doc so that we can execute genName() on it
    name = name or doc.genName() # this is important!
    dt = doc.doctype
    debug(dt + " " + name)
    if frappe.db.exists(dt, name): # check if it exists
        doc = frappe.get_cached_doc(dt, name)
        # if yes, we have to retrieve the original, otherwise it will complain in doc.save()
        # that we are trying to insert a Document that already exists...
        for key in docDict.keys(): # set the attributes
            setattr(doc, key, docDict[key])
        doc.save() # this will also call doc.genName() internally to check for existing... again
        for key in metadata:
            frappe.db.set_value(dt, name, key, metadata[key])
    else:
        doc.insert()
        for key in metadata:
            frappe.db.set_value(dt, name, key, metadata[key])

def setDocumentWithName(docDict, name):
    def setProps(doc, docDict):
        for key in docDict.keys():
            setattr(doc, key, docDict[key])

    dt = docDict["doctype"]
    if not frappe.db.exists(dt, name):
         debug("creating doctype {}/{}".format(dt, name))
         doc = frappe.new_doc(dt)
         setProps(doc, docDict)
         doc.insert()
    else:
        doc = frappe.get_doc(dt, name)
        setProps(doc, docDict)
        doc.save()

class SwitchFallThrough(Exception):
    "Raised when nothing matched a switch Expression"
    def __init__(self,toBeTested):
        self.toBeTested = toBeTested
        self.message = "You didn't cover all cases, nothing matched {}".format(self.toBeTested)

class Switcher():
    def __init__(self, switchMapF):
        from collections import OrderedDict as d
        import functools

        def prepare(tupl):
            """(1,2,3) gets split into ((1,2), 3) as preparation for Ordered dict
            This is to make it easiyer for the writer to write"""
            return (tupl[:len(tupl)-1], tupl[len(tupl)-1])

        self._ = "____extremelyUnlikeLyString_"
        self.switchList = switchMapF(self._)
        fistTupleLength = len(self.switchList[0])
        assert functools.reduce(lambda acc,v: (len(v) == fistTupleLength) and acc, self.switchList), "All Condition Tuples must have the same length"
        self.switchMap = d(map(prepare, self.switchList))

    def tester(self, acc, testTuple):
        """gets mapped over the zip of the values in the test tuple to
        the positionally corresponing tupleenty in the key of the switch map"""
        toBeTested = testTuple[0]
        testedAgainst = testTuple[1]
        return acc and (testedAgainst == self._ or toBeTested == testedAgainst)

    def switch(self, *toBeTested):
        import functools
        for testedAgainst in self.switchMap:
            assert len(toBeTested) == len(testedAgainst), "your switch arguments number must match your keys in your switchmap. {} doesn't match {}".format(testedAgainst, toBeTested)
            if functools.reduce(self.tester, zip(toBeTested, testedAgainst), True):
                return self.switchMap[testedAgainst]
        raise SwitchFallThrough()

def add_role_profile(roleProfileName, roles):
    if not frappe.db.exists("Role Profile", roleProfileName):
        doc = frappe.new_doc("Role Profile")
        doc.role_profile = roleProfileName
        for role in roles:
            doc.append('roles', {
                'role': role
            })
        doc.insert()
        frappe.db.commit()
