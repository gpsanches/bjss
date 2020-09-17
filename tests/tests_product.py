# coding=utf-8

import unittest

from utils import PackageTypes
from app.product import Product


class ProductTestCase(unittest.TestCase):
    def setUp(self):
        self.product = Product()

    def tearDown(self):
        self.product = list()

    def test_add_product_complete(self):
        self.assertEqual(self.product.products, dict())
        self.product.add_product(name="Soup", price=0.65, package_type=PackageTypes.TIN.value)
        self.product.add_product(name="Bread", price=0.8, package_type=PackageTypes.LOAF.value)
        self.assertDictEqual(self.product.products, {'Soup': {'price': 0.65, 'package_type': 'tin'},
                                                     'Bread': {'price': 0.8, 'package_type': 'loaf'}})

    def test_get_list_items(self):
        self.assertEqual(self.product.products, dict())
        self.product.add_product(name="Bread", price=0.8, package_type=PackageTypes.LOAF.value)
        self.assertDictEqual(self.product.products, {'Bread': {'price': 0.8, 'package_type': 'loaf'}})

    def test_get_product_existent(self):
        self.product.add_product(name="Soup", price=0.65, package_type=PackageTypes.TIN.value)
        self.product.add_product(name="Bread", price=0.8, package_type=PackageTypes.LOAF.value)
        self.product.add_product(name="Milk", price=0.8, package_type=PackageTypes.BOTTLE.value)
        self.assertDictEqual(self.product.get_product('Milk'), {'name': 'Milk', 'price': 0.8, 'package_type': 'bottle'})

    def test_get_product_not_existent(self):
        self.product.add_product(name="Soup", price=0.65, package_type=PackageTypes.TIN.value)
        self.product.add_product(name="Bread", price=0.8, package_type=PackageTypes.LOAF.value)
        self.product.add_product(name="Milk", price=0.8, package_type=PackageTypes.BOTTLE.value)
        self.assertFalse(self.product.get_product('Banana'))

    def test_remove_product(self):
        self.product.add_product(name="Soup", price=0.65, package_type=PackageTypes.TIN.value)
        self.product.add_product(name="Bread", price=0.8, package_type=PackageTypes.LOAF.value)
        self.product.add_product(name="Milk", price=1.8, package_type=PackageTypes.BOTTLE.value)
        self.product.remove_product('Milk')
        self.assertDictEqual(self.product.products, {'Soup': {'price': 0.65, 'package_type': 'tin'},
                                                     'Bread': {'price': 0.8, 'package_type': 'loaf'}})
