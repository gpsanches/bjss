# coding=utf-8

import unittest

from utils import DiscountTypes, PackageTypes
from app.product import Product
from app.discount import Discount


class DiscountTestCase(unittest.TestCase):
    def setUp(self):
        self.discount = Discount()
        self.product = Product()
        self.product.add_product(name="Grape", price=1.0, package_type=PackageTypes.TIN.value)
        self.product.add_product(name="Milk", price=2.0, package_type=PackageTypes.BOTTLE.value)

    def tearDown(self):
        self.discount = list()
        self.product = list()

    def test_add_discount(self):
        self.assertListEqual(self.discount.discount, list())
        self.discount.add(10, self.product.get_product('Grape'), _when_field=None, _when_op=None, _when_value=None,
                          _to=None, discount_type=DiscountTypes.PERCENTAGE.name, description="Grape 10 % off")
        self.assertListEqual(self.discount.discount, [{'product': 'Grape', 'value': 10, '_when_field': None,
                                                       '_when_op': None, '_when_value': None, '_to': None,
                                                       'discount_type': 'PERCENTAGE', 'description': 'Grape 10 % off'}])

    def test_remove_all_discount(self):
        self.assertListEqual(self.discount.discount, list())
        self.discount.add(10, self.product.get_product('Grape'), _when_field=None, _when_op=None, _when_value=None,
                          _to=None, discount_type=DiscountTypes.PERCENTAGE.name, description="Grape 10 % off")
        self.assertListEqual(self.discount.discount, [{'product': 'Grape', 'value': 10, '_when_field': None,
                                                       '_when_op': None, '_when_value': None, '_to': None,
                                                       'discount_type': 'PERCENTAGE', 'description': 'Grape 10 % off'}])
        self.discount.remove_all_discount()
        self.assertListEqual(self.discount.discount, list())

    def test_get_discount_by_product_name_existent(self):
        self.assertListEqual(self.discount.discount, list())
        self.discount.add(10, self.product.get_product('Grape'), _when_field=None, _when_op=None, _when_value=None,
                          _to=None, discount_type=DiscountTypes.PERCENTAGE.name, description="Grape 10 % off")
        self.discount.add(20, self.product.get_product('Milk'), _when_field=None, _when_op=None, _when_value=None,
                          _to=None, discount_type=DiscountTypes.PERCENTAGE.name, description="milk 20 % off")
        self.assertListEqual(self.discount.discount, [{'product': 'Grape', 'value': 10, '_when_field': None,
                                                       '_when_op': None, '_when_value': None, '_to': None,
                                                       'discount_type': 'PERCENTAGE', 'description': 'Grape 10 % off'},
                                                      {'product': 'Milk', 'value': 20, '_when_field': None,
                                                       '_when_op': None, '_when_value': None, '_to': None,
                                                       'discount_type': 'PERCENTAGE', 'description': 'milk 20 % off'}])
        self.assertDictEqual(self.discount.get_by_product('Milk'), {'product': 'Milk', 'value': 20, '_when_field': None,
                                                                    '_when_op': None, '_when_value': None, '_to': None,
                                                                    'discount_type': 'PERCENTAGE',
                                                                    'description': 'milk 20 % off'})

    def test_get_discount_by_product_name_not_existent(self):
        self.assertListEqual(self.discount.discount, list())
        self.discount.add(10, self.product.get_product('Grape'), _when_field=None, _when_op=None, _when_value=None,
                          _to=None, discount_type=DiscountTypes.PERCENTAGE.name, description="Grape 10 % off")
        self.discount.add(20, self.product.get_product('Milk'), _when_field=None, _when_op=None, _when_value=None,
                          _to=None, discount_type=DiscountTypes.PERCENTAGE.name, description="milk 20 % off")
        self.assertListEqual(self.discount.discount, [{'product': 'Grape', 'value': 10, '_when_field': None,
                                                       '_when_op': None, '_when_value': None, '_to': None,
                                                       'discount_type': 'PERCENTAGE',
                                                       'description': 'Grape 10 % off'},
                                                      {'product': 'Milk', 'value': 20, '_when_field': None,
                                                       '_when_op': None, '_when_value': None, '_to': None,
                                                       'discount_type': 'PERCENTAGE',
                                                       'description': 'milk 20 % off'}])
        self.assertFalse(self.discount.get_by_product('Banana'))

    def test_get_all_discount(self):
        self.assertListEqual(self.discount.discount, list())
        self.discount.add(10, self.product.get_product('Grape'), _when_field=None, _when_op=None, _when_value=None,
                          _to=None, discount_type=DiscountTypes.PERCENTAGE.name, description="Grape 10 % off")
        self.discount.add(20, self.product.get_product('Milk'), _when_field=None, _when_op=None, _when_value=None,
                          _to=None, discount_type=DiscountTypes.PERCENTAGE.name, description="milk 20 % off")
        self.assertListEqual(self.discount.get_all(), [{'product': 'Grape', 'value': 10, '_when_field': None,
                                                        '_when_op': None, '_when_value': None, '_to': None,
                                                        'discount_type': 'PERCENTAGE',
                                                        'description': 'Grape 10 % off'},
                                                       {'product': 'Milk', 'value': 20, '_when_field': None,
                                                        '_when_op': None, '_when_value': None, '_to': None,
                                                        'discount_type': 'PERCENTAGE',
                                                        'description': 'milk 20 % off'}])
