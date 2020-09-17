# coding=utf-8

import unittest

from utils import PackageTypes
from app.product import Product
from app.discount import Discount
from app.cart import Cart


class CartTestCase(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()

        self.product = Product()
        self.product.add_product(name="Soup", price=0.65, package_type=PackageTypes.TIN.value)
        self.product.add_product(name="Bread", price=0.80, package_type=PackageTypes.LOAF.value)
        self.product.add_product(name="Milk", price=1.3, package_type=PackageTypes.BOTTLE.value)
        self.product.add_product(name="Apple", price=1.0, package_type="bag")

        self.discount = Discount()
        self.discount.add(
            product=self.product.get_product('Apple'), value=10,
            description="Apples have 10% off their normal price this week")

        self.discount.add(
            product=self.product.get_product('Soup'), value=50, _to=self.product.get_product('Bread'),
            _when_field="qty", _when_op="ge", _when_value="2",
            description="Buy 2 tins of soup and get a loaf of bread for half price")

    def tearDown(self):
        self.cart = list()
        self.discount = list()
        self.product = list()

    def test_add_cart(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.assertListEqual(self.cart.items, [{'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 1}])
        self.assertEqual(self.cart.subtotal, 0.8)
        self.cart.add_item(self.product.get_product('Apple'))
        self.assertListEqual(self.cart.items, [{'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 1},
                                               {'name': 'Apple', 'price': 1.0, 'package_type': 'bag', 'qty': 1}])
        self.assertEqual(self.cart.subtotal, 1.8)

    def test_add_cart_already_existent(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.assertEqual(self.cart.subtotal, 0.8)
        self.assertListEqual(self.cart.items, [{'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 1}])
        self.cart.add_item(self.product.get_product('Bread'))
        self.assertEqual(self.cart.subtotal, 1.6)
        self.assertListEqual(self.cart.items, [{'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 2}])
        self.cart.add_item(self.product.get_product('Bread'))
        self.assertEqual(round(self.cart.subtotal, 2), 2.4)
        self.assertListEqual(self.cart.items, [{'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 3}])

    def test_get_items(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.assertListEqual(self.cart.get_items(), [{'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 1}])

    def test_find_item_by_product(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.cart.add_item(self.product.get_product('Apple'))
        self.assertDictEqual(self.cart.find_item(self.product.get_product('Bread')), {'name': 'Bread', 'price': 0.8,
                                                                                      'package_type': 'loaf', 'qty': 1})

    def test_find_item_by_name(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.cart.add_item(self.product.get_product('Apple'))
        self.assertTupleEqual(self.cart.find_item_by_name('Bread'), ({'name': 'Bread', 'price': 0.8,
                                                                      'package_type': 'loaf', 'qty': 1}, 0))

    def test_find_item_by_name(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.cart.add_item(self.product.get_product('Apple'))
        self.assertTupleEqual(self.cart.find_item_by_name('Bread'), ({'name': 'Bread', 'price': 0.8,
                                                                      'package_type': 'loaf', 'qty': 1}, 0))

    def test_remove_item(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.cart.add_item(self.product.get_product('Apple'))
        self.cart.remove_item('Apple')
        self.assertListEqual(self.cart.get_items(), [{'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 1}])

    def test_remove_item_not_existent(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.cart.add_item(self.product.get_product('Apple'))
        self.cart.remove_item('Banana')
        self.assertListEqual(self.cart.get_items(), [{'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 1},
                                                     {'name': 'Apple', 'price': 1.0, 'package_type': 'bag', 'qty': 1}])

    def test_remove_all(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.cart.add_item(self.product.get_product('Apple'))
        self.cart.remove_all()
        self.assertListEqual(self.cart.get_items(), list())

    def test_add_total_without_discount(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.cart.apply_discount(self.discount)
        self.assertListEqual(self.cart.get_items(), [{'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 1}])
        self.assertEqual(round(self.cart.total, 2), 0.8)

    def test_add_total_with_10_percent_discount(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Apple'))
        self.cart.apply_discount(self.discount)
        self.assertListEqual(self.cart.get_items(), [{'discount_value': 0.1, 'name': 'Apple', 'new_price': 0.9,
                                                      'price': 1.0, 'package_type': 'bag', 'qty': 1}])
        self.assertEqual(round(self.cart.total, 2), 0.9)

    def test_add_total_with_10_percent_discount_and_product_without(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.cart.add_item(self.product.get_product('Apple'))
        self.cart.apply_discount(self.discount)
        self.assertListEqual(self.cart.get_items(), [{'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 1},
                                                     {'name': 'Apple', 'price': 1.0, 'package_type': 'bag', 'qty': 1,
                                                      'discount_value': 0.1, 'new_price': 0.9}])
        self.assertEqual(len(self.cart.get_items()), 2)
        self.assertEqual(round(self.cart.total, 2), 1.7)

    def test_add_total_with_50_percent_discount_and_product_without(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.cart.add_item(self.product.get_product('Soup'), 2)
        self.cart.apply_discount(self.discount)
        self.assertListEqual(self.cart.get_items(), [{'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 1,
                                                      'discount_value': 0.4, 'new_price': 0.4},
                                                     {'name': 'Soup', 'price': 0.65, 'package_type': 'tin', 'qty': 2}])
        self.assertEqual(len(self.cart.get_items()), 2)
        self.assertEqual(round(self.cart.total, 2), 1.7)

    def test_add_all_products_with_discount_and_without_discount(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.cart.add_item(self.product.get_product('Soup'), 2)
        self.cart.add_item(self.product.get_product('Apple'), 2)
        self.cart.add_item(self.product.get_product('Milk'), 1)
        self.cart.add_item(self.product.get_product('Milk'), 1)
        self.cart.apply_discount(self.discount)
        self.assertListEqual(self.cart.get_items(), [
            {'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 1, 'discount_value': 0.4, 'new_price': 0.4},
            {'name': 'Soup', 'price': 0.65, 'package_type': 'tin', 'qty': 2},
            {'name': 'Apple', 'price': 1.0, 'package_type': 'bag', 'qty': 2, 'discount_value': 0.2, 'new_price': 1.8},
            {'name': 'Milk', 'price': 1.3, 'package_type': 'bottle', 'qty': 2}])

        self.assertEqual(len(self.cart.get_items()), 4)
        self.assertEqual(round(self.cart.subtotal, 2), 6.7)
        self.assertEqual(round(self.cart.total, 2), 6.1)

    def test_result_with_discount(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Apple'))
        self.cart.apply_discount(self.discount)
        self.assertListEqual(self.cart.get_items(), [
            {'name': 'Apple', 'price': 1.0, 'package_type': 'bag', 'qty': 1, 'discount_value': 0.1, 'new_price': 0.9}])
        self.assertEqual(round(self.cart.total, 2), 0.9)
        self.assertDictEqual(self.cart.result(),
                             {'subtotal': '£: 1.0', 'discount': ['Apple 10 % off: -10p'], 'total': '£: 0.9'})

    def test_result_with_more_than_one_discount(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Apple'))
        self.cart.add_item(self.product.get_product('Bread'))
        self.cart.add_item(self.product.get_product('Soup'), 2)
        self.cart.apply_discount(self.discount)
        self.assertListEqual(
            self.cart.get_items(),
            [{'name': 'Apple', 'price': 1.0, 'package_type': 'bag', 'qty': 1, 'discount_value': 0.1, 'new_price': 0.9},
             {'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 1, 'discount_value': 0.4, 'new_price': 0.4},
             {'name': 'Soup', 'price': 0.65, 'package_type': 'tin', 'qty': 2}])
        self.assertEqual(round(self.cart.total, 2), 2.6)
        print(self.cart.result())
        self.assertDictEqual(
            self.cart.result(),
            {'subtotal': '£: 3.1', 'discount': ['Apple 10 % off: -10p', 'Bread 50 % off: -50p'], 'total': '£: 2.6'})

    def test_result_without_discount(self):
        self.assertListEqual(self.cart.items, list())
        self.assertEqual(self.cart.total, 0.0)
        self.assertEqual(self.cart.subtotal, 0.0)
        self.cart.add_item(self.product.get_product('Bread'))
        self.cart.apply_discount(self.discount)
        self.assertListEqual(self.cart.get_items(), [{'name': 'Bread', 'price': 0.8, 'package_type': 'loaf', 'qty': 1}])
        self.assertEqual(round(self.cart.total, 2), 0.8)
        self.assertDictEqual(self.cart.result(),
                             {'subtotal': '£: 0.8', 'discount': ['no offers available'], 'total': '£: 0.8'})
