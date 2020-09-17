# coding=utf-8

from utils import DiscountTypes
from app.product import Product


class Cart(Product):

    def __init__(self):
        self.items = list()
        self.subtotal = 0.0
        self.total = 0.0
        self.currency_symbol = "£"
        self.currency_code = "GBP"
        self.discounts = list()

    def get_items(self):
        return self.items

    def find_item(self, product):
        for product_name in self.items:
            if product.get('name') == product_name.get('name'):
                return product_name
        return False

    def find_item_by_name(self, product_name):
        for idx, item in enumerate(self.items):
            if product_name == item.get('name'):
                return item, idx
        return False, None

    def add_item(self, product, qty=1):
        item, idx = self.find_item_by_name(product.get('name'))
        if item:
            self.items[idx].update(dict(qty=item.get('qty') + qty))
        else:
            product.update(dict(qty=qty))
            self.items.append(product)

        self.subtotal += round(product.get('price') * qty, 2)

    def remove_item(self, name):
        item, idx = self.find_item_by_name(name)
        if item:
            self.items.pop(idx)
            self.total -= round(item.get('price') * item.get('qty'), 2)

    def remove_all(self):
        self.items = list()
        self.total = 0.0

    def add_total(self, price, qty):
        self.total += round(price * qty, 2)

    def add_total_with_discount(self, item_cart, discount_rule, remove_old_price=False):
        if remove_old_price:
            self.total -= round(item_cart.get('price') * item_cart.get('qty'), 2)

        discount_value = round(item_cart.get('price') * item_cart.get('qty') * (discount_rule.get('value') / 100), 2)
        grand_total = round(item_cart.get('price') * item_cart.get('qty') - discount_value, 2)

        self.discounts.append("{0} {1} {2} off: -{1}p".format(item_cart.get('name'), discount_rule.get('value'),
                                                              DiscountTypes.PERCENTAGE.value))
        item_cart.update(discount_value=discount_value, new_price=grand_total)
        self.total += round(grand_total, 2)

    def apply_discount(self, discount_obj):
        self.discounts = list()
        for item_cart in self.items:
            discount_rule = discount_obj.get_by_product(item_cart.get('name'))
            if not discount_rule:
                self.add_total(item_cart.get('price'), item_cart.get('qty'))
                continue

            if not discount_rule.get('_when_field'):
                self.add_total_with_discount(item_cart, discount_rule)
                continue

            item_find_cart = self.find_item(discount_rule.get('_to'))
            if item_find_cart \
                    and discount_rule.get('_when_field') \
                    and discount_rule.get('_when_op') \
                    and discount_rule.get('_when_value'):
                if discount_rule.get('_when_op') == 'ge':
                    if item_cart.get(discount_rule.get('_when_field')) >= int(discount_rule.get('_when_value')):
                        self.add_total_with_discount(item_find_cart, discount_rule, True)
                    self.add_total(item_cart.get('price'), item_cart.get('qty'))
                continue

            self.add_total(item_cart.get('price'), item_cart.get('qty'))

        if not self.discounts:
            self.discounts.append('no offers available')

    def result(self):
        return dict(subtotal="{}: {}".format(self.currency_symbol, round(self.subtotal, 2)),
                    discount=self.discounts,
                    total="{}: {}".format(self.currency_symbol, round(self.total, 2)))
