import pandas as pd
import xml.etree.ElementTree as ET


if __name__ == '__main__':
    tree = ET.parse('column1.xml')
    root = tree.getroot()
    print('Root tag is ',root.tag)
    # for index,child in enumerate(root.iter()):
    #     #  only root nodes
    #     if  len(child) == 0:
    #         print(index,child.tag,',',child.attrib,'=',child.text)
    target_xpath = './InvHeader/Totals/MonAmnt[@Type="TaxAmount"]'
    target_tag = root.find(target_xpath)
    print(target_tag.tag,target_tag.attrib,target_tag.text)
