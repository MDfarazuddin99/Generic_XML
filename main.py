import xml.etree.ElementTree as ET
import pandas as pd
tree = ET.parse('OnDemandBillRun-9910995780.xml')

root = tree.getroot()

for element in root.iter():
    print(element.tag,',',element.attrib,'=',element.text)
# for element in root.iter():
#     print(element.tag,',',element.attrib,'=',element.text)

path = input()
a = root.findall(path)

csv = dict()

for index,child in enumerate(a):
    print('\t|-->',index,child.tag,',',child.attrib,'=',child.text)
    csv[child.tag] = child.text

print(csv)
csv = pd.DataFrame(csv,index=[0])
file_name = input()
csv.to_csv('{}.csv'.format(file_name))
for child in root.iter('MonAmnt'):
    print(child.tag,child.attrib,child.tag)
