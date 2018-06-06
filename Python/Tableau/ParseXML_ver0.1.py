# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

def func_datasource(datasource):
    for elem in datasource:
        if elem.get("name") == "Parameters":
            key = 1
            parameters = {}
            print("Parameters")
            for datasourceChild in elem:
                if datasourceChild.tag == "column":
                    parameters[key] = {}
                    parameters[key]["caption"] = datasourceChild.get("caption")
                    parameters[key]["value"] = datasourceChild.get("value")
                    parameters[key]["member"] = []
                    for columnChild in datasourceChild:
                        if columnChild.tag == "members":
                            for member in columnChild:
                                parameters[key]["member"].append(member.get("value"))
                    key = key + 1
            print(parameters)
        else:
            key = 1
            datasource = {}
            #print(elem.get("caption"))
            for connection in elem.getiterator("connection"):
                columns = []
                for metadatarecords in connection.getiterator("metadata-records"):
                    for metadatarecord in metadatarecords.getiterator("metadata-record"):
                        if metadatarecord.get("class") == "column":
                            column = {}
                            for metadata in metadatarecord:
                                tag = metadata.tag
                                print (tag)
                                if tag == 'local-name':
                                    column["localname"] = metadata.text
                                if tag == 'caption':
                                    column["caption"] = metadata.text
                                elif tag == 'family':
                                    column["family"] = metadata.text
                                elif tag == 'local-type':
                                    column["localtype"] = metadata.text
                            columns.append(column)
                    print(columns)

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
    print('start tag')
    print(child.tag)
    if child.tag == "datasources":
        func_datasource(child)
    elif child.tag == "worksheets":
        func_worksheets(child)
    elif child.tag == "dashboards":
        func_dashboards(child)