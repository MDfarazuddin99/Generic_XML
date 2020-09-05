import pandas as pd
import xml.etree.ElementTree as ET


def load_interface(file_path):
    tree = ET.parse(file_path)
    root = ET.getroor(tree)
    return ET.tag


if __name__ == '__main__':
    # print(load_interface('interface.xml'))
    tree = ET.parse('interface.xml')
    root = tree.getroot()
    print('Root tag is ',root.tag)
    for index,child in enumerate(root.iter()):
        if  child.attrib != {}:
            print(index,child.tag,',',child.attrib,'=',child.text)
