from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def get_leaf_elements(path_to_file):
    '''
    Function to get all the leaf elements from an interface input xml File.
    Leaf elements are those which dont have any child elements.
    '''
    soup = BeautifulSoup(open(path_to_file), 'xml')
    all_elements = soup.find_all()
    leaf_element_indices = list()
    for index,i in enumerate(all_elements):
        if len(i.findChildren()) == 0:
            leaf_element_indices.append(index)
    leaf_elements = [all_elements[i] for i in leaf_element_indices]
    return leaf_elements

def get_path(element):
    '''
    Returns the Xpath as a string which will be used to extract data from Bill files
    '''
    to_remove = ['[document]', 'body', 'html']
    path = [element.name]+ [e.name for e in element.parents if e.name not in to_remove]
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
        file = 'interface.xml'
        leaf_elements = get_leaf_elements(file)
        for leaf in leaf_elements:
            print(get_path(leaf))
