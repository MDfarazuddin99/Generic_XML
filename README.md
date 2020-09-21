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
### Corresponding CSV file for above case
|FIELD1|TypeOfBill|BillStartDate                |BillEndDate                  |InvoiceAmount|Tax      |TaxOnTax|ExemptedTax|TotalAmount|
|------|----------|-----------------------------|-----------------------------|-------------|---------|--------|-----------|-----------|
|0     |Regular   |2020-03-01T01:00:00.000+01:00|2020-09-04T07:38:57.762+02:00|0.000000     |0.000000 |0.000000|0.000000   |0.000000   |
|1     |Regular   |2020-05-10T03:00:01.000+02:00|2020-07-22T09:56:21.189+02:00|50.000000    |22.500000|0       |0.0        |72.500000  |
|2     |Regular   |2020-07-22T11:06:39.545+02:00|2020-07-22T11:16:57.594+02:00|1.000000     |0.450000 |0       |0.0        |1.450000   |
|3     |Regular   |2020-07-22T09:39:45.526+02:00|2020-07-22T09:41:56.400+02:00|34.482758    |15.517242|0       |0.0        |50.000000  |


### Interface files with action atrribute (action="count", action="sum")
```
<Interface>
  <Invoice>
    <Contracts>
    	<Contract action="count">NoOfContracts</Contract>
    </Contracts>
  </Invoice>
</Interface>
```
It's Corresponding xpath
```
Interface/Invoice/Contracts/Contract[@action="count"]
```
