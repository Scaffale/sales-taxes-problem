import re
import unittest

class taxCalculator(object):
	# Items to tax
	items = []

	def __init__(self):
		super(taxCalculator, self).__init__()
	
	def addItem(self, item):
		self.items.append(item)

class taxTest(unittest.TestCase):
	
	# test 1
	def test_1(self):
		tax = taxCalculator()
		tax.addItem('Hello test')
		self.assertEqual(len(tax.items), 1)

unittest.main()