import re
import unittest

class taxCalculator(object):
	# Items to tax
	items = []
	taxedItems = []

	def __init__(self):
		super(taxCalculator, self).__init__()
		self.items = []
		self.taxedItems = []
	
	def addItem(self, item):
		self.items.append(item)
	
	def calculateSingleTax(self, item):
		return item

	def calculateTax(self):
		for item in self.items:
			self.taxedItems.append(self.calculateSingleTax(item))


# UnitTest for the class taxCalculator
class taxTest(unittest.TestCase):
	
	def test_addItem_adds_item_to_items(self):
		tax = taxCalculator()
		tax.addItem('Hello test')
		self.assertEqual(len(tax.items), 1)

	def test_calculate_tax_slould_move_items_to_taxedItems(self):
		tax = taxCalculator()
		tax.addItem('1 book at 12.49')
		tax.calculateTax()
		self.assertEqual(tax.taxedItems[0], '1 book at 12.49')

unittest.main()