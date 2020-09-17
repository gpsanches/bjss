# coding=utf-8

from utils import DiscountTypes


class Discount:

    def __init__(self):
        self.discount = list()

    def add(self, value, product, _when_field=None, _when_op=None, _when_value=None, _to=None,
            discount_type=DiscountTypes.PERCENTAGE.name, description=None):
        self.discount.append(dict(
            product=product['name'], value=value, _when_field=_when_field, _when_op=_when_op, _when_value=_when_value,
            _to=_to, discount_type=discount_type, description=description))

    def remove_all_discount(self):
        self.discount = list()

    def get_by_product(self, product_name):
        for i in self.discount:
            if i.get('product') == product_name:
                return i
        return False

    def get_all(self):
        return self.discount
