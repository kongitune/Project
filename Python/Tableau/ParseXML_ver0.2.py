# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

def func_datasource(datasource):
    for elem in datasource:
        if elem.get("name") == "Parameters":
            print("---- Parameters ----")
            key = 1
            parameters = {}
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
            
            # Datasource Definition
            print("---- metadata definition ----")
            metadatarecords = elem.findall('connection/metadata-records/')
            columns = []
            for metadatarecord in metadatarecords:
                if metadatarecord.get("class") == "column":
                    column = {}
                    for metadata in metadatarecord:
                        tag = metadata.tag
                        if tag == 'local-name':
                            column["local-name"] = metadata.text
                        elif tag == 'local-type':
                            column["localtype"] = metadata.text
                    columns.append(column)
            print(columns)
            
            # Caliculation Fields
            print("---- Caliculations ----")
            caliculations = []
            for columnChild in elem:
                if columnChild.tag == "column" and columnChild.get("caption") is not None:
                    caliculations.append(columnChild.attrib)
            
            print(caliculations)


def func_worksheet(worksheet):
    print('---- worksheet ----')
    
    # sheet name
    sheetName = worksheet.get("name")
    print(sheetName)
    
    # using datasource
    datasources = worksheet.findall('table/view/datasources/')
    for datasourcesChild in datasources:
        print(datasourcesChild.get('caption'))
    
    # filter
    view = worksheet.findall('table/view/')
    for viewChild in view:
        if viewChild.tag == 'filter':
            print(viewChild.attrib)
    
    # marks
    encodings = worksheet.findall('table/panes/pane/encodings/')
    for encodingsChild in encodings:
        if encodingsChild.tag == 'color':
            print('color')
            print(encodingsChild.get("column"))
        elif encodingsChild.tag == 'size':
            print('size')
            print(encodingsChild.get("column"))
        elif encodingsChild.tag == 'lod':
            print('lod')  # Detail
            print(encodingsChild.get("column"))
        elif encodingsChild.tag == 'tooltip':
            print('tooltip')
            print(encodingsChild.get("column"))
        elif encodingsChild.tag == 'text':
            print('text')  # Label
            print(encodingsChild.get("column"))
    
    # axis
    table = worksheet.findall('table/')
    for tableChild in table:
        if tableChild.tag == 'rows':
            print('horizontal axis')
            print(tableChild.text)
        if tableChild.tag == 'cols':
            print('vertical axis')
            print(tableChild.text)
    
def func_dashboard(dashboard):
    print('---- dashbord ----')
    
    # dashbord name
    print(dashboard.get("name"))
    
    # worksheet name used in the dashboard
    nestZone = 'zones/zone/'
    zone = dashboard.findall(nestZone)
    #for zoneChild in zone:
    #    if zoneChild.tag == 'name' None:
    #        break
    #    elif zoneChild.tag in None and zoneChild.get('Name') is None:
    #        print(zoneChild.get('Name'))
        
    nestZone = nestZone + 'zone/'
    print(nestZone)

def func_datasources(datasources):
    for datasource in datasources:
        func_datasource(datasource)

def func_worksheets(worksheets):
    for worksheet in worksheets:
        func_worksheet(worksheet)

def func_dashboards(dashboards):
    for dashboard in dashboards:
        func_dashboard(dashboard)

# Main process
fp = open("Superstore2.twb","r",encoding="utf-8")
content = fp.read()

# root tag attribute
root = ET.fromstring(content)
print(root.tag, root.attrib)

# Child Layer tag attribute
for child in root:
    if child.tag == "datasources":
        func_datasource(child)
    elif child.tag == "worksheets":
        func_worksheets(child)
    elif child.tag == "dashboards":
        func_dashboards(child)
