# coding=utf-8

class Product:

    def __init__(self):
        self.products = dict()

    def get_list_items(self):
        return self.products

    def get_product(self, name):
        if self.products.get(name):
            product = dict(name=name)
            product.update(self.products.get(name))
            return product
        return False

    def add_product(self, name, price, package_type):
        self.products[name] = dict(price=price, package_type=package_type)

    def remove_product(self, name):
        return self.products.pop(name)
