import xml.etree.ElementTree as ET

file = open('page_text.html', 'w')

def func_datasource(datasource):
    for elem in datasource:
        if elem.get("name") == "Parameters":
            print("---- Parameters ----")
            key = 1
            file.write('<table border="1">\n')
            file.write('    <caption>Prameter</caption>\n')
            for datasourceChild in elem:
                if datasourceChild.tag == "column":
                    file.write('    <tr>\n')
                    file.write('        <td>' + datasourceChild.get("caption") + '</td>\n')
                    file.write('        <td>' + datasourceChild.get("value") + '</td>\n')
                    file.write('        <td>')
                    for columnChild in datasourceChild:
                        if columnChild.tag == "members":
                            for member in columnChild:
                                file.write(member.get("value"))
                    key = key + 1
                    file.write('</td>\n')
                    file.write('    </tr>\n')
            file.write('</table>\n')
        else:
            
            # Datasource Definition
            print("---- metadata ----")
            metadatarecords = elem.findall("connection/metadata-records/")
            columns = []
            file.write('<table border="1">\n')
            file.write('    <caption>data</caption>\n')
            for metadatarecord in metadatarecords:
                if metadatarecord.get("class") == "column":
                    column = {}
                    for metadata in metadatarecord:
                        # print(metadata.attrib)
                        if metadata.tag == 'local-name':
                            file.write('    <tr>\n')
                            file.write('        <td>'+ metadata.text + '</td>\n')
                        elif metadata.tag == 'local-type':
                            file.write('        <td>' + metadata.text + '</td>\n')
                            file.write('    </tr>\n')
                    columns.append(column)
            file.write('</table>\n')
            
            # Caliculation Fields
            print("---- Caliculations ----")
            caliculations = []
            file.write('<table border="1">\n')
            file.write('    <caption>Caliculation Fields</caption>\n')
            for columnChild in elem:
                if columnChild.tag == "column" and columnChild.get("caption") is not None:
                    caliculations.append(columnChild.attrib)
                    file.write('    </tr>\n')
                    file.write('        <td>' + columnChild.get("caption") + '</td>\n')
                    file.write('        <td>' + columnChild.get("datatype") + '</td>\n')
                    file.write('        <td>' + columnChild.get("role") + '</td>\n')
                    file.write('    </tr>\n')
            file.write('</table>\n')
            print(caliculations)


def func_worksheet(worksheet):
    print('---- worksheet ----')
    
    # sheet name
    sheetName = worksheet.get("name")
    file.write('<p>' + sheetName + '</p>')
    
    # using datasource
    datasources = worksheet.findall('table/view/datasources/')
    for datasourcesChild in datasources:
        file.write('<p>' + datasourcesChild.get('caption') + '</p>')
    
    # filter
    view = worksheet.findall('table/view/')
    file.write('<table border="1">\n')
    file.write('    <caption>filter</caption>\n')
    for viewChild in view:
        if viewChild.tag == 'filter':
            print(viewChild.attrib)
            file.write('    <tr>\n')
            file.write('        <td>' + viewChild.get("class") + '</td>\n')
            file.write('        <td>' + viewChild.get("column") + '</td>\n')
            file.write('    </tr>\n')
    file.write('</table>\n')
    
    # marks
    encodings = worksheet.findall('table/panes/pane/encodings/')
    file.write('<table border="1">\n')
    file.write('    <caption>marks</caption>\n')
    for encodingsChild in encodings:
        if encodingsChild.tag == 'color':
            file.write('    <tr>\n')
            file.write('        <td>color</td>\n')
            file.write('        <td>' + encodingsChild.get("column") + '</td>\n')
            file.write('    </tr>\n')
        elif encodingsChild.tag == 'size':
            file.write('    <tr>\n')
            file.write('        <td>size</td>\n')
            file.write('        <td>' + encodingsChild.get("column") + '</td>\n')
            file.write('    </tr>\n')
        elif encodingsChild.tag == 'lod':  # Detail
            file.write('    <tr>\n')
            file.write('        <td>Detail</td>\n')
            file.write('        <td>' + encodingsChild.get("column") + '</td>\n')
            file.write('    </tr>\n')
        elif encodingsChild.tag == 'tooltip':
            file.write('    <tr>\n')
            file.write('        <td>tooltip</td>\n')
            file.write('        <td>' + encodingsChild.get("column") + '</td>\n')
            file.write('    </tr>\n')
        elif encodingsChild.tag == 'text':  # Label
            file.write('    <tr>\n')
            file.write('        <td>label</td>\n')
            file.write('        <td>' + encodingsChild.get("column") + '</td>\n')
            file.write('    </tr>\n')
    file.write('</table>\n')
    
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
    
    # worksheet names used in the dashboard
    
    zone = dashboard.findall('.zones//zone[@name]')    
    for zoneChild in zone:
        print(zoneChild.get('name'))

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
fp = open("Superstore.twb","r",encoding="utf-8")
content = fp.read()

# root tag attribute
root = ET.fromstring(content)
print(root.tag, root.attrib)

# Child Layer tag attribute
for rootChild in root:
    if rootChild.tag == "datasources":
        func_datasource(rootChild)
    elif rootChild.tag == "worksheets":
        func_worksheets(rootChild)
    elif rootChild.tag == "dashboards":
        func_dashboards(rootChild)

file.close()