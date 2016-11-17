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
			self.taxedItems.append(self.calculateSingleTax(item))

	def calculateSingleTax(self, item):
		if self.mustBeTaxed(item):
			price = re.findall('\d+.\d+', item)
			try:
				# sobsitute price and replace ' at ' with ': '
				return item.replace(' at ' + price[0], ': ' + self.taxPrice(price[0]), 1)
			except Exception as e:
				return item
		else:
			# if item does not have taxes still needs to change the ' at '
			return item.replace(' at ', ': ', 1)

	def taxPrice(self, priceString):
		# Convert string into float, execute 10% tax, save tax, back to string
		priceFloat = float(priceString)
		taxOnPrice = priceFloat * 0.1
		self.salesTaxes += taxOnPrice
		taxedPrice = round(priceFloat * 1.1, 2)
		return str(taxedPrice)

	def mustBeTaxed(self, item):
		freeTaxRE = 'books?|chocolates?|headache|pills?'
		freeTax = re.findall(freeTaxRE, item, flags=re.IGNORECASE)
		if len(freeTax) > 0:
			return False
		return True


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

unittest.main()