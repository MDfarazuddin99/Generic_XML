from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
def get_root_elements(path_to_file):
    soup = BeautifulSoup(open(path_to_file), 'lxml')
    all_elements = soup.find_all()
    count_element_indices = [len(list(a.parents)) for a in all_elements]
    leaf_element_indices = list()

    for index,i in enumerate(all_elements):
        if len(i.findChildren()) == 0:
            leaf_element_indices.append(index)
    leaf_elements = [all_elements[i] for i in leaf_element_indices]

    return leaf_elements

def get_path(element):
    to_remove = ['document', 'body', 'html']
    path = [element.name]+ [e.name for e in element.parents if e.name not in to_remove]
    if 'action' in element.attrs.keys():
        element.attrs.pop('action')
    attribs = [element.attrs] + [e.attrs for e in element.parents if e.name not in to_remove]
    path = path[::-1]
    attribs = attribs[::-1]
    del path[0]
    del attribs[0]
    xpath = ''
    for index,val in enumerate(path):
        xpath += path[index]
        for key,val in attribs[index].items():
            xpath += '[@' + str(str(key) + '=\"' + str(val) + '\"]')
        xpath += '/'
    return xpath[:-1]

if __name__ == "__main__":
        file = 'Columns/Count/column9.xml'
        bill_file = 'Bills\OnDemandBillRun-9910995780.xml'
        roots = get_root_elements(file)
        tree = ET.parse(bill_file)
        b = tree.getroot()
        for root in roots:
            a = get_path(root)
            print(a)
        #     c = b.find(a)
        #     print(c)
