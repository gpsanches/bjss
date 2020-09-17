# coding=utf-8

from utils import PackageTypes
from app.product import Product
from app.discount import Discount
from app.cart import Cart


if __name__ == '__main__':
    items = Product()
    items.add_product(name="Soup", price=0.65, package_type=PackageTypes.TIN.value)
    items.add_product(name="Bread", price=0.80, package_type=PackageTypes.LOAF.value)
    items.add_product(name="Milk", price=1.3, package_type=PackageTypes.BOTTLE.value)
    items.add_product(name="Apple", price=1.0, package_type=PackageTypes.BAG.value)

    print("---- Products list")
    print(items.get_list_items())

    discount = Discount()
    discount.add(
        product=items.get_product('Apple'), value=10, description="Apples have 10% off their normal price this week")

    discount.add(
        product=items.get_product('Soup'), value=50, _to=items.get_product('Bread'), _when_field="qty",
        _when_op="ge", _when_value="2", description="Buy 2 tins of soup and get a loaf of bread for half price")

    cart = Cart()

    user_cart = input("Add name of products and ',' qty if more than one:")
    for user in user_cart.split(' '):
        product, *qty = user.split(",")
        product = product.lower().capitalize()
        qty = int(qty[0]) if qty else 1
        if not items.get_product(product):
            print("\n Product: {}, not exist in product list!".format(product))
            continue

        cart.add_item(items.get_product(product), qty)

    cart.apply_discount(discount)

    print("---- Cart result")
    print(cart.result())
