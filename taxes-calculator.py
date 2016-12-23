import re
import unittest

class taxCalculator(object):
	items = []
	taxedItems = []
	salesTaxes = 0.0
	total = 0.0
	# 'Costants' for the taxes
	salesTax = 0.1
	importationTax = 0.05

	def addItem(self, item):
		self.items.append(item)

	def clear(self):
		self.items = []
		self.taxedItems = []
		self.salesTaxes = 0.0
		self.total = 0.0

	def calculateTax(self):
		for item in self.items:
			taxedItem = self.calculateSingleTax(item)
			self.taxedItems.append(taxedItem)
		self.taxedItems.append('Sales Taxes: ' + Helper.numberToString(self.salesTaxes))
		self.taxedItems.append('Total: ' + Helper.numberToString(self.total))

	def calculateSingleTax(self, item):
		itemWithoutAt = Helper.replaceAt(item)
		tax = 0.0
		if Helper.mustBeTaxed(itemWithoutAt):
			tax += self.salesTax
		if Helper.isImported(itemWithoutAt):
			tax += self.importationTax
		return self.taxPrice(itemWithoutAt, tax)

	def taxPrice(self, item, tax):
		price = re.findall('\d+.\d+', item)
		# Convert string into float, execute tax%, save, back to string
		try:
			priceFloat = float(price[0])
			if Helper.thereIsPromo(self.items) and Helper.isPromo(item) == False:
				priceFloat *= .9
			if Helper.thereIsPromo(self.items) and len(self.items) == 1:
				priceFloat *= .9
			totalTax = priceFloat * tax
			if Helper.isImported(item):
				totalTax = Helper.roundToFive(totalTax)
			self.salesTaxes += totalTax
			taxedPrice = round(priceFloat + totalTax, 2)
			self.total += taxedPrice
			return Helper.arrangeImported(item.replace(price[0], Helper.numberToString(taxedPrice), 1))
		except:
			return item # In case the string is not of the correct format nothing happens

class Helper(object):
	@staticmethod
	def numberToString(numb):
		return str("%.2f" % numb)

	@staticmethod
	def replaceAt(item):
		return item.replace(' at ', ': ', 1)

	@staticmethod
	def roundToFive(number):
		twoDecimalPrecision = (number * 100) % 10
		if twoDecimalPrecision == 5 or twoDecimalPrecision == 0:
			return number
		return number - twoDecimalPrecision / 100 + (0.05 if twoDecimalPrecision < 5 else 0.1)

	@staticmethod
	def mustBeTaxed(item):
		freeTaxRE = 'books?|chocolates?|headache|pills?'
		return len(re.findall(freeTaxRE, item, flags=re.IGNORECASE)) == 0

	@staticmethod
	def isImported(item):
		return len(re.findall('imported', item, flags=re.IGNORECASE)) > 0

	@staticmethod
	def arrangeImported(item):
		number = re.findall('\d+ ', item)
		imported = re.findall('imported ', item, flags=re.IGNORECASE)
		try: # from '1 box of imported chocolates at 11.25' to '1 imported box of chocolates: 11.25'
			if len(number) > 0:
				return item.replace(imported[0], '', 1).replace(number[0], number[0] + imported[0], 1)
			return imported[0] + item.replace(imported[0], '', 1)
		except:
			return item # In case the string is not properly fomratted

	@staticmethod
	def isPromo(item):
		return len(re.findall('promo', item, flags=re.IGNORECASE)) > 0

	@staticmethod
	def thereIsPromo(items):
		for item in items:
			if Helper.isPromo(item):
				return True
		return False

	# @staticmethod
	# def allpyDiscount(items, promo):
	# 	for item in items:
	# 		if (item != promo):
	# 			number = Helper.findPrice(item)

	# @staticmethod
	# def findPrice(item):
	# 	return Helper.float(re.findall('\d+.\d+', item)[0])

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
		self.assertEqual(self.tax.taxedItems[0], '1 imported box of chocolates: 11.85')

	def test_imported_items_should_move_the_imported_word(self):
		self.tax.clear()
		self.tax.addItem('1 box of imported chocolates at 11.25')
		self.tax.calculateTax()
		self.assertEqual(self.tax.taxedItems[0], '1 imported box of chocolates: 11.85')

	def test_Input_1(self):
		self.tax.clear()
		self.tax.addItem('1 book at 12.49')
		self.tax.addItem('1 music CD at 14.99')
		self.tax.addItem('1 chocolate bar at 0.85')
		self.tax.calculateTax()
		results = []
		results.append('1 book: 12.49')
		results.append('1 music CD: 16.49')
		results.append('1 chocolate bar: 0.85')
		results.append('Sales Taxes: 1.50')
		results.append('Total: 29.83')
		self.assertEqual(self.tax.taxedItems, results)

	def test_Input_2(self):
		self.tax.clear()
		self.tax.addItem('1 imported box of chocolates at 10.00')
		self.tax.addItem('1 imported bottle of perfume at 47.50')
		self.tax.calculateTax()
		results = []
		results.append('1 imported box of chocolates: 10.50')
		results.append('1 imported bottle of perfume: 54.65')
		results.append('Sales Taxes: 7.65')
		results.append('Total: 65.15')
		self.assertEqual(self.tax.taxedItems, results)

	def test_Input_3(self):
		self.tax.clear()
		self.tax.addItem('1 imported bottle of perfume at 27.99')
		self.tax.addItem('1 bottle of perfume at 18.99')
		self.tax.addItem('1 packet of headache pills at 9.75')
		self.tax.addItem('1 box of imported chocolates at 11.25')
		self.tax.calculateTax()
		results = []
		results.append('1 imported bottle of perfume: 32.19')
		results.append('1 bottle of perfume: 20.89')
		results.append('1 packet of headache pills: 9.75')
		results.append('1 imported box of chocolates: 11.85')
		results.append('Sales Taxes: 6.70')
		results.append('Total: 74.68')
		self.assertEqual(self.tax.taxedItems, results)

	def test_Promo_Product(self):
		self.tax.clear()
		self.tax.addItem('1 promo product at 50.00')
		self.tax.calculateTax()
		self.assertEqual(self.tax.taxedItems[0], '1 promo product: 49.50')

	def test_isPromoTest(self):
		self.assertEqual(True, Helper.isPromo('1 promo product at 45'))

	def test_thereIsPromoTest(self):
		lista = ['1 promo product at 45.00', '1 product at 45.00', '1 product at 45.00']
		self.assertEqual(True, Helper.thereIsPromo(lista))

	def test_Promo_doppio(self):
		self.tax.clear()
		self.tax.addItem('1 promo product at 50.00')
		self.tax.addItem('1 music CD at 14.99')
		self.tax.calculateTax()
		results = []
		results.append('1 promo product: 55.00')
		results.append('1 music CD: 14.84')
		results.append('Sales Taxes: 6.35')
		results.append('Total: 69.84')
		self.assertEqual(self.tax.taxedItems, results)
unittest.main()
