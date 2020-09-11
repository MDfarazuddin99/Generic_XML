from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
def get_root_elements(path_to_file):
    soup = BeautifulSoup(open(path_to_file), 'xml')
    all_elements = soup.find_all()

    count_element_indices = [len(list(a.parents)) for a in all_elements]

    absolute_roots_index = min(
        (index for index, element in enumerate(count_element_indices)
            if element == max(count_element_indices)
        )
    )

    return all_elements[absolute_roots_index:]

def get_path(element):
    to_remove = ['[document]', 'body', 'html']
    path = [element.name] + [e.name for e in element.parents if e.name not in to_remove]
    attribs = list()
    for e in element.parents:
         if e.name not in to_remove:
            # print(e.attrs)
            attribs.append(e.attrs)

    path = path[::-1]
    del path[0]
    attribs += [element.attrs]
    # print(attribs)
    del attribs[0]
    xpath = ''
    for index,val in enumerate(path):
        xpath += path[index]
        for key,val in attribs[index].items():
            xpath += '[@' + str(str(key) + '=\"' + str(val) + '\"]')
        xpath += '/'
    return xpath


if __name__ == "__main__":
        file = 'Columns/column7.xml'
        roots = get_root_elements(file)
        # print(roots)
        tree = ET.parse(file)
        b = tree.getroot()
        for root in roots:
            a = get_path(root)
            print(a)
            # print(b.find(a).attrib)
