import xml.etree.ElementTree as ET

def getresults():
    tree = ET.parse('det.out')
    root = tree.getroot()
    lanespeed = []
    for child in root:
        x = child.attrib
        y = x.get('id')
                # print(y)
        if y == 'det_0_F':
            z = float(x.get('harmonicMeanSpeed'))
            #print("Lane 1 Speed:",z)
            lanespeed.append(z)
        if y == 'det_1_F':
            z = float(x.get('harmonicMeanSpeed'))
            #print("Lane 2 Speed:",z)
            lanespeed.append(z)
        if y == 'det_2_F':
            z = float(x.get('harmonicMeanSpeed'))
            #print("Lane 3 Speed:",z)
            lanespeed.append(z)
    SUM = sum(lanespeed)
    AVG = SUM/len(lanespeed)
    return AVG


