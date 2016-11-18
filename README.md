# sales-taxes-problem
This code answers the following problem:

## PROBLEM: SALES TAXES

**Basic sales tax** is applicable at a rate of **10%** on all goods, **except** books, food, and medical products that are exempt. **Import duty** is an additional sales tax applicable on all imported goods at a rate of 5%, with no exemptions.

When I purchase items I receive a receipt which lists the name of all the items and their price (including tax), finishing with the total cost of the items, and the total amounts of sales taxes paid. The rounding rules for sales tax are that for a tax rate of n%, a shelf price of p contains (np/100 rounded up to the nearest 0.05) amount of sales tax.

Write an application that prints out the receipt details for these shopping baskets...

```
INPUT:

Input 1:
1 book at 12.49
1 music CD at 14.99
1 chocolate bar at 0.85

Input 2:
1 imported box of chocolates at 10.00
1 imported bottle of perfume at 47.50

Input 3:
1 imported bottle of perfume at 27.99
1 bottle of perfume at 18.99
1 packet of headache pills at 9.75
1 box of imported chocolates at 11.25

OUTPUT

Output 1:
1 book: 12.49
1 music CD: 16.49
1 chocolate bar: 0.85
Sales Taxes: 1.50
Total: 29.83

Output 2:
1 imported box of chocolates: 10.50
1 imported bottle of perfume: 54.65
Sales Taxes: 7.65
Total: 65.15

Output 3:
1 imported bottle of perfume: 32.19
1 bottle of perfume: 20.89
1 packet of headache pills: 9.75
1 imported box of chocolates: 11.85
Sales Taxes: 6.70
Total: 74.68
```

## Requirements
Built for **Python 2.7.10**
To download and install python follow any guide you can find
[python.org](https://www.python.org/download/releases/2.7/)
To run it:
```
python taxes-calculator.py
```

## How to run it
In the code there are unitTest, to avoid the tests comment the line (should be the last one)
```
unittest.main()
```

The object works this way:
* Init
```
tax = taxCalculator()
```
* Add items (add Strings)
```
tax.addItem('1 imported bottle of perfume at 47.50')
...
```
* Calculate tax
```
tax.calculateTax()
```
* Read the data (it's an array of Strings)
```
tax.taxedItems
```
Note that the *calculateTax()* method adds two lines to the *taxedItems* array:
```
Sales Taxes: 6.70
Total: 74.68
```
* Clear the data
```
tax.clear()
```
This is essential if you run *calculateTax()* because the method just add lines to the array, and it does not clear it

## How it internally works
Once you add the item such as ```1 box of imported chocolates at 11.25``` if you run the calculateTax method this happen:
1. Replace the *' at '* part of the item with *': '*
2. If the item has to be taxed (so if the string does not contains *book*, *chocolate*, *pill* or *headache*) add 10% tax
3. If the item is imported (so if the string contains the word *imported*) add 5% tax
4. Modify the item price based on the tax
5. If the item is imported round the price to nearest 0.05 value
6. Arrange the item in order to have the word *imported* right after the number
So at the end you will have the item like ```1 imported box of chocolates: 11.85```

### Remember that:
If you run *calculateTax()* the array of taxed items will have at the end the two lines for **Sales Taxes** and **Total**.
The method *clear()* will clear all items