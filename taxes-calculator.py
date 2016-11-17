import re
import unittest

class taxCalculator(object):
	# Items to tax
	items = []
	taxedItems = []
	salesTaxes = 0.0

	def __init__(self):
		super(taxCalculator, self).__init__()
		self.items = []
		self.taxedItems = []
		self.salesTaxes = 0.0
	
	def addItem(self, item):
		self.items.append(item)

	def calculateTax(self):
		for item in self.items:
			taxedItem = self.calculateSingleTax(item)
			self.taxedItems.append(taxedItem)

	def calculateSingleTax(self, item):
		itemWithoutAt = self.replaceAt(item)
		if self.mustBeTaxed(itemWithoutAt):
			return self.taxImportation(self.taxPrice(itemWithoutAt, 0.1))
		return self.taxImportation(itemWithoutAt)

	def taxPrice(self, item, tax):
		price = re.findall('\d+.\d+', item)
		# Convert string into float, execute 10% tax, save tax, back to string
		try:
			priceFloat = float(price[0])
			taxOnPrice = priceFloat * tax
			self.salesTaxes += taxOnPrice
			taxedPrice = round(priceFloat * (1 + tax), 2)
			return item.replace(price[0], str("%.2f" % taxedPrice), 1)
		except:
			return item

	def mustBeTaxed(self, item):
		freeTaxRE = 'books?|chocolates?|headache|pills?'
		freeTax = re.findall(freeTaxRE, item, flags=re.IGNORECASE)
		if len(freeTax) > 0:
			return False
		return True

	def taxImportation(self, item):
		if len(re.findall('imported', item, flags=re.IGNORECASE)) > 0:
			return self.taxPrice(item, 0.05)
		return item

	def replaceAt(self, item):
		return item.replace(' at ', ': ', 1)

# UnitTest for the class taxCalculator
class taxTest(unittest.TestCase):
	
	def test_addItem_adds_item_to_items(self):
		tax = taxCalculator()
		tax.addItem('Hello test')
		self.assertEqual(len(tax.items), 1)

	def test_calculateTax_slould_move_items_to_taxedItems(self):
		tax = taxCalculator()
		tax.addItem('1 music CD at 14.99')
		tax.calculateTax()
		self.assertEqual(tax.taxedItems[0], '1 music CD: 16.49')

	def text_calculateSingleTax_should_increase_number(self):
		tax = taxCalculator()
		increasedItem = tax.calculateSingleTax('1 music CD at 14.99')
		self.assertEqual(increasedItem, '1 music CD: 16.49')

	def test_calculateTax_slould_increment_price(self):
		tax = taxCalculator()
		tax.addItem('1 music CD at 14.99')
		tax.calculateTax()
		self.assertEqual(tax.taxedItems[0], '1 music CD: 16.49')

	def test_calculateTax_should_not_increment_for_books(self):
		tax = taxCalculator()
		tax.addItem('1 book at 12.49')
		tax.calculateTax()
		self.assertEqual(tax.taxedItems[0], '1 book: 12.49')

	def test_imported_items_should_have_more_tax(self):
		tax = taxCalculator()
		tax.addItem('1 imported box of chocolates at 10.00')
		tax.calculateTax()
		self.assertEqual(tax.taxedItems[0], '1 imported box of chocolates: 10.50')

unittest.main()