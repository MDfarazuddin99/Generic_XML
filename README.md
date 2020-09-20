# Generic_XML_Data_Extraction
Generic program to read multiple xml files and convert it into a single csv file.

![Block Diagram](https://github.com/MDfarazuddin99/Generic_XML/blob/master/Readme_fig1.png)

### Sample interface.xml file (Most Simple Case)
```
<Interface>
  <Invoice>
    <InvHeader>
      <InvoiceType>TypeOfBill</InvoiceType>
      <PeriodStart>BillStartDate</PeriodStart>
      <PeriodEnd>BillEndDate</PeriodEnd>
      <Totals>
        <MonAmnt Type="InvoiceAmount">InvoiceAmount</MonAmnt>
        <MonAmnt Type="TaxAmount">Tax</MonAmnt>
        <MonAmnt Type="TaxOnTaxAmount">TaxOnTax</MonAmnt>
        <MonAmnt Type="ExemptedTaxAmount">ExemptedTax</MonAmnt>
        <MonAmnt Type="TotalAmount">TotalAmount</MonAmnt>
      </Totals>
    </InvHeader>
  </Invoice>
</Interface>
```
