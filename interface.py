import os
import pandas as pd
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from my_parser import get_leaf_elements,get_path


if __name__ == '__main__':
    # Listing all Bill Files and Column Files
    Bill_folder = 'Bills'
    Bill_files = os.listdir(Bill_folder)
    Bill_files = [os.path.join(Bill_folder,i) for i in Bill_files]
    # print('All Bill Files\n',Bill_files)
    interface_file_path = 'interface.xml'
    leaf_elements = get_leaf_elements(interface_file_path)
    column_xpaths = list()
    column_xpaths_action = list()
    column_xpaths_action_sum = [
    'FinancialTransactions/FinancialTransactionGroups/FinancialTransactionGroup[FinancialHeaderType="adjustment"]/FinancialHeaders/FinancialHeader/Amounts/MonAmnt[@Type="OPEN_CREDIT"]',
    ]

    for leaf_element in leaf_elements:
        if '[@action="count"]' in get_path(leaf_element):
            column_xpaths_action.append(get_path(leaf_element))
        else:
            column_xpaths.append(get_path(leaf_element))

    interface_tree= ET.parse('interface.xml')
    interface_tree_root = interface_tree.getroot()
    Bill_dict = dict()

    for xpath in column_xpaths + column_xpaths_action:
        print(xpath)
        element = interface_tree_root.find(xpath)
        # print(element.tag,element.attrib,element.text)
        Bill_dict[element.text] = list()

    for xpath in column_xpaths:
        column = interface_tree_root.find(xpath)
        column_name = column.text
        for Bill_file in Bill_files:
            tree_bill = ET.parse(Bill_file)
            root_bill = tree_bill.getroot()
            node_bill = root_bill.find(xpath)
            try:
                Bill_dict[column_name].append(node_bill.text)
            except:
                Bill_dict[column_name].append(None)

    for xpath in column_xpaths_action:
        column = interface_tree_root.find(xpath)
        column_name = column.text
        for Bill_file in Bill_files:
            tree_bill = ET.parse(Bill_file)
            root_bill = tree_bill.getroot()
            node_bill = root_bill.findall(xpath.replace('[@action="count"]',''))
            try:
                Bill_dict[column_name].append(len(node_bill))
            except:
                Bill_dict[column_name].append(None)

    Bill_dict['Adjustment'] = list()

    for Bill_file in Bill_files:
            tree_bill = ET.parse(Bill_file)
            root_bill = tree_bill.getroot()
            node_bills = root_bill.findall(column_xpaths_action_sum[0])
            try:
                sum=0
                for node in node_bills:
                    # print('--->',node.text)
                    sum += float(node.text)
                Bill_dict['Adjustment'].append(sum)
            except:
                Bill_dict['Adjustment'].append(None)
                
    print(Bill_dict)
    Bill_df = pd.DataFrame(Bill_dict)
    Bill_df.to_csv('./Data.csv')
