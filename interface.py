import os
import pandas as pd
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
# Calling functions from Custom module name = my_parser.py
from my_parser import get_leaf_elements,get_path


if __name__ == '__main__':
    # Listing all Bill Files and Column Files
    Bill_folder = 'Bills'
    Bill_files = os.listdir(Bill_folder)
    Bill_files = [os.path.join(Bill_folder,i) for i in Bill_files]
    interface_file_path = 'interface.xml'
    leaf_elements = get_leaf_elements(interface_file_path)
    column_xpaths = list()
    column_xpaths_action_count = list()
    column_xpaths_action_sum = list()
    column_dict = dict()
    Bill_dict = dict()

    for leaf_element in leaf_elements:
        xpath = get_path(leaf_element)
        # For complicated xpaths in interface file with action = count
        if '[@action="count"]' in  xpath and 'xpath' not in xpath:
            tree = ET.parse(interface_file_path)
            root = tree.getroot()
            element = root.find(xpath)
            Bill_dict[element.text] = list()
            column_xpaths_action_count.append(xpath)
        #For simple xpaths in interface file with action = sum
        elif '[@action="sum"]' in xpath and 'xpath' not in xpath:
            tree = ET.parse(interface_file_path)
            root = tree.getroot()
            element = root.find(xpath)
            Bill_dict[element.text] = list()
            column_xpaths_action_sum.append(xpath)
        # For complicated xpaths in interface file
        elif 'xpath' in get_path(leaf_element):
            tree = ET.parse(interface_file_path)
            root = tree.getroot()
            elements = root.findall(xpath)
            for element in elements:
                Bill_dict[element.tag] = list()
                column_dict[element.tag] = element.text
        # For simple xpaths in interface file
        else:
            tree = ET.parse(interface_file_path)
            root = tree.getroot()
            element = root.find(xpath)
            Bill_dict[element.text] = list()
            column_xpaths.append(xpath)

    interface_tree= ET.parse('interface.xml')
    interface_tree_root = interface_tree.getroot()

#   For simple xpaths
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

#   For simple xpath with action = count
    for xpath in column_xpaths_action_count:
        column = interface_tree_root.find(xpath)
        column_name = column.text
        for Bill_file in Bill_files:
            tree_bill = ET.parse(Bill_file)
            root_bill = tree_bill.getroot()
            node_bills = root_bill.findall(xpath.replace('[@action="count"]',''))
            try:
                Bill_dict[column_name].append(len(node_bills))
            except:
                Bill_dict[column_name].append(None)

#   For simple xpath with action = sum
    for xpath in column_xpaths_action_sum:
        column = interface_tree_root.find(xpath)
        column_name = column.text
        for Bill_file in Bill_files:
            tree_bill = ET.parse(Bill_file)
            root_bill = tree_bill.getroot()
            node_bills = root_bill.findall(xpath.replace('[@action="sum"]',''))
            try:
                sum = 0
                for node in node_bills:
                    sum += float(node.text)
                Bill_dict[column_name].append(sum)
            except:
                Bill_dict[column_name].append(None)

#   For the complicated xpaths passed in interface file
    for key,val in column_dict.items():
        for Bill_file in Bill_files:
            tree_bill = ET.parse(Bill_file)
            root_bill = tree_bill.getroot()
            if '[@action="sum"]' in val:
                node_bills = root_bill.findall(val.replace('[@action="sum"]',''))
                try:
                    sum=0
                    for node in node_bills:
                        sum += float(node.text)
                    Bill_dict[key].append(sum)
                except:
                    Bill_dict[key].append(None)
            elif '[@action="count"]' in val:
                node_bills = root_bill.findall(val.replace('[@action="count"]',''))
                try:
                    Bill_dict[key].append(len(node_bills))
                except:
                    Bill_dict[key].append(None)
# __________________________________Not Generic for LastMonthPending and LastMonthBill__________________________________
    # PeriodStart_xpath = 'Invoice/InvHeader/PeriodStart'
    # LastMonthPending_path = 'FinancialTransactions/FinancialTransactionGroups/FinancialTransactionGroup[FinancialHeaderType="Invoice"]/FinancialHeaders/FinancialHeader/Amounts/MonAmnt[@Type="OPEN_DEBIT"]'
    # LastMonthBill_path = 'FinancialTransactions/FinancialTransactionGroups/FinancialTransactionGroup[FinancialHeaderType="Invoice"]/FinancialHeaders/FinancialHeader/Amounts/MonAmnt[@Type="ORIGINAL_DEBIT"]'
    # BillingEndDate_xpath = 'FinancialTransactions/FinancialTransactionGroups/FinancialTransactionGroup[FinancialHeaderType="Invoice"]/FinancialHeaders/FinancialHeader/FinancialHeaderCharacteristics/Characteristic[@key="BillingEndDate"]'
    #
    # Bill_dict['LastMonthPending'] = list()
    # Bill_dict['LastMonthBill'] = list()
    #
    # for Bill_file in Bill_files:
    #     tree_bill = ET.parse(Bill_file)
    #     root_bill = tree_bill.getroot()
    #     node_bills = root_bill.findall(xpath)
    #     try:
    #         PeriodStart = tree_bill.find(PeriodStart_xpath).text
    #         BillingEndDates = [i.text for i in tree_bill.findall(BillingEndDate_xpath)]
    #         LastMonthPending = [i.text for i in tree_bill.findall(LastMonthPending_path)]
    #         sum = 0
    #         for index,date in enumerate(BillingEndDates):
    #             if (PeriodStart[0:10] == date[0:10]):
    #                 sum += float(LastMonthPending[index])
    #         Bill_dict['LastMonthPending'].append(sum)
    #     except:
    #         print('->LastMonthPending Error<-')
    #
    # for Bill_file in Bill_files:
    #     tree_bill = ET.parse(Bill_file)
    #     root_bill = tree_bill.getroot()
    #     node_bills = root_bill.findall(xpath)
    #     try:
    #         PeriodStart = tree_bill.find(PeriodStart_xpath).text
    #         BillingEndDates = [i.text for i in tree_bill.findall(BillingEndDate_xpath)]
    #         LastMonthBill = [i.text for i in tree_bill.findall(LastMonthBill_path)]
    #         sum=0
    #         for index,date in enumerate(BillingEndDates):
    #             if (PeriodStart[0:10] == date[0:10]):
    #                 sum += float(LastMonthBill[index])
    #         Bill_dict['LastMonthBill'].append(sum)
    #     except:
    #         print('->LastMonthBill Error<-')


    print(Bill_dict)
    Bill_df = pd.DataFrame(Bill_dict)
    Bill_df.to_csv('./Data.csv')
