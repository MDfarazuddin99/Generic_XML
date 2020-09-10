import os
import pandas as pd
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

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
    path = path[::-1]
    del path[0]
    attribs = [element.attrs] + [e.name for e in element.parents if e.name not in to_remove]
    attribs = attribs[::-1]
    del attribs[0]
    xpath = ''
    for index,val in enumerate(path):
        xpath += path[index]
        try:
            for key,val in attribs[index].items():
                xpath += '[@' + str(str(key) + '=\"' + str(val) + '\"]')
        except:
            xpath += '/'
    return './' + xpath


if __name__ == '__main__':
    # Listing all Bill Files and Column Files
    Bill_folder = 'Bills'
    Bill_files = os.listdir(Bill_folder)
    Bill_files = [os.path.join(Bill_folder,i) for i in Bill_files]
    print('All Bill Files\n',Bill_files)
    Column_folder = 'Columns'
    Column_files = os.listdir(Column_folder)
    Column_files = [os.path.join(Column_folder,i) for i in Column_files]
    print('All Column Files\n',Column_files)
    #  Getting Xpath for all the Column_files and appending into a list
    Column_Xpaths = list()
    for column in Column_files:
        roots = get_root_elements(column)
        for root in roots:
            # print(get_path(root))
            Column_Xpaths.append(get_path(root))
    # print('Corresponding Column Xpaths\n',Column_Xpaths)
    # Initalizing a dictionary to store keys as values in The Xpath
    Bill_dict = dict()
    for Column_file,xpath in zip(Column_files,Column_Xpaths):
        print(Column_file,xpath)
        tree = ET.parse(Column_file)
        root = tree.getroot()
        node = root.find(xpath)
        Bill_dict[node.text] = []
        # print(node.tag,node.attrib,node.text)
    print('Bill Dictionary\n',Bill_dict)
    # Nested Loop for filling up the Dictionary
    for Column_file,xpath in zip(Column_files,Column_Xpaths):
        print(Column_file,xpath)
        tree_column = ET.parse(Column_file)
        root_column = tree_column.getroot()
        node_column = root_column.find(xpath)
        column_name = node_column.text
        for Bill_file in Bill_files:
            print(Bill_file)
            tree_bill = ET.parse(Bill_file)
            root_bill = tree_bill.getroot()
            node_bill = root_bill.find(xpath)
            Bill_dict[column_name].append(node_bill.text)
    # print(Bill_dict)
    Bill_df = pd.DataFrame(Bill_dict)
    Bill_df.to_csv('./Data.csv')
