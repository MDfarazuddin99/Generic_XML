import xml.etree.ElementTree as ET
import pandas as pd
tree = ET.parse('./Bills/OnDemandBillRun-9910995780.xml')

root = tree.getroot()
totals_tag = root.find('Invoice')
for child in totals_tag.iter():
    print(child.tag,child.attrib,child.text)
