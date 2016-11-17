import re
import unittest

class taxCalculator(object):
	# Items to tax
	items = []
	taxedItems = []
	salesTaxes = 0.0

	def addItem(self, item):
		self.items.append(item)

	def calculateTax(self):
		for item in self.items:
			taxedItem = self.calculateSingleTax(item)
			self.taxedItems.append(taxedItem)

	def calculateSingleTax(self, item):
		itemWithoutAt = self.replaceAt(item)
		tax = 0.0
		if self.mustBeTaxed(itemWithoutAt):
			tax += 0.1
		if self.isImported(itemWithoutAt):
			tax += 0.05
		return self.taxPrice(itemWithoutAt, tax)

	def taxPrice(self, item, tax):
		price = re.findall('\d+.\d+', item)
		# Convert string into float, execute tax%, save, back to string
		try:
			priceFloat = float(price[0])
			taxOnPrice = priceFloat * tax
			self.salesTaxes += taxOnPrice
			taxedPrice = round(priceFloat * (1 + tax), 2)
			if self.isImported(item):
				taxedPrice = self.roundToFive(taxedPrice)
			return item.replace(price[0], str("%.2f" % taxedPrice), 1)
		except:
			return item

	def mustBeTaxed(self, item):
		freeTaxRE = 'books?|chocolates?|headache|pills?'
		return (len(re.findall(freeTaxRE, item, flags=re.IGNORECASE)) == 0)

	def isImported(self, item):
		return (len(re.findall('imported', item, flags=re.IGNORECASE)) > 0)

	def roundToFive(self, number):
		twoDecimalPrecision = (number * 100) % 10
		if twoDecimalPrecision == 5 or twoDecimalPrecision == 0:
			return number
		if twoDecimalPrecision == 2 or twoDecimalPrecision == 6:
			return self.roundToFive(number + 0.03)
		return self.roundToFive(number + 0.01)

	def replaceAt(self, item):
		return item.replace(' at ', ': ', 1)

	def clear(self):
		self.items = []
		self.taxedItems = []
		self.salesTaxes = 0.0

# UnitTest for the class taxCalculator
class taxTest(unittest.TestCase):
	tax = taxCalculator()

	def test_addItem_adds_item_to_items(self):
		self.tax.clear()
		self.tax.addItem('Hello test')
		self.assertEqual(len(self.tax.items), 1)

	def test_calculateTax_slould_move_items_to_taxedItems(self):
		self.tax.clear()
		self.tax.addItem('1 chocolate bar at 0.85')
		self.tax.calculateTax()
		self.assertEqual(self.tax.taxedItems[0], '1 chocolate bar: 0.85')

	def text_calculateSingleTax_should_increase_number(self):
		increasedItem = self.tax.calculateSingleTax('1 music CD at 14.99')
		self.assertEqual(increasedItem, '1 music CD: 16.49')

	def test_calculateTax_slould_increment_price(self):
		self.tax.clear()
		self.tax.addItem('1 music CD at 14.99')
		self.tax.calculateTax()
		self.assertEqual(self.tax.taxedItems[0], '1 music CD: 16.49')

	def test_calculateTax_should_not_increment_for_books(self):
		self.tax.clear()
		self.tax.addItem('1 book at 12.49')
		self.tax.calculateTax()
		self.assertEqual(self.tax.taxedItems[0], '1 book: 12.49')

	def test_imported_items_should_have_more_tax(self):
		self.tax.clear()
		self.tax.addItem('1 imported box of chocolates at 10.00')
		self.tax.calculateTax()
		self.assertEqual(self.tax.taxedItems[0], '1 imported box of chocolates: 10.50')

	def test_random_stirng_should_not_raise_error(self):
		self.tax.clear()
		self.tax.addItem('foobar foo bar foo')
		self.tax.calculateTax()
		self.assertEqual(self.tax.taxedItems[0], 'foobar foo bar foo')
	
	def test_taxes_should_be_done_at_once(self):
		self.tax.clear()
		self.tax.addItem('1 imported bottle of perfume at 47.50')
		self.tax.calculateTax()
		self.assertEqual(self.tax.taxedItems[0], '1 imported bottle of perfume: 54.65')

	def test_imported_items_should_round_to_the_nearest_5(self):
		self.tax.clear()
		self.tax.addItem('1 box of imported chocolates at 11.25')
		self.tax.calculateTax()
		self.assertEqual(self.tax.taxedItems[0], '1 box of imported chocolates: 11.85')

unittest.main()