# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

def func_datasource(datasource):
    for elem in datasource:
        print(elem.tag)
        if elem.get("name") == "Parameters":
            # Parameters
            key = 1
            parameters = {}
            print("Parameters ---------------")
            for datasourceChild in elem:
                if datasourceChild.tag == "column":
                    parameters[key] = {}
                    parameters[key]["caption"] = datasourceChild.get("caption")
                    parameters[key]["datatype"] = datasourceChild.get("datatype")
                    parameters[key]["role"] = datasourceChild.get("role")
                    parameters[key]["value"] = datasourceChild.get("value")
                    parameters[key]["member"] = []
                    for columnChild in datasourceChild:
                        if columnChild.tag == "members":
                            for member in columnChild:
                                parameters[key]["member"].append(member.get("value"))
                    key = key + 1
            print(parameters)
        else:
            # Datasource Definition
            print("metadata definition --------------")
            key = 1
            datasource = {}
            metadatarecord = elem.findall('connection/relation/columns/')
            for mdt in metadatarecord:
                print(mdt.attrib)
                print(mdt.get("name"))

            
            # Caliculation Field
            print("caliculation --------------")
            key = 1
            datasource = {}
            caliculations = []
            for columnChild in elem:
                caliculation = {}
                if columnChild.tag == "column" and columnChild.get("caption") is not None:
                    caliculation["caption"] = columnChild.get("caption")
                    caliculation["name"] = columnChild.get("name")
                    caliculation["datatype"] = columnChild.get("datatype")
                    caliculation["role"] = columnChild.get("role")
                    caliculations.append(caliculation)
            
            print(caliculations)

def func_worksheet(worksheet):
    print(worksheet.get("name"))

def func_dashboard(dashboard):
    print(dashboard.get("name"))

def func_datasources(datasources):
    for datasource in datasources:
        func_datasource(datasource)

def func_worksheets(worksheets):
    for worksheet in worksheets:
        func_worksheet(worksheet)

def func_dashboards(dashboards):
    for dashboard in dashboards:
        func_dashboard(dashboard)

fp = open("Superstore2.twb","r",encoding="utf-8")
content = fp.read()

root = ET.fromstring(content)

# 最上位階層のタグと中身
print(root.tag,root.attrib)

# 子階層のタグと中身
for child in root:
    if child.tag == "datasources":
        func_datasource(child)
    elif child.tag == "worksheets":
        func_worksheets(child)
    elif child.tag == "dashboards":
        func_dashboards(child)