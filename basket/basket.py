from decimal import Decimal

from django.conf import settings
from django.http import HttpRequest
from django.db.models import Prefetch

from store.models import Product


class Basket:
    """
    A base Basket class, providing some default behaviours that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request: HttpRequest):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)

        # check if there is a basket session for this user,
        # if not create a session
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}

        self.basket = basket

    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)

        # check if the product is in the basket
        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        else:
            self.basket[product_id] = {"price": str(product.regular_price), "qty": int(qty)}

        # saving the session data
        self.save()

    def update(self, product_id, product_qty):
        """
        Update values in session data
        """
        product_id = str(product_id)
        qty = product_qty

        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty

        self.save()

    def delete(self, product_id):
        """
        Delete item from session data
        """
        product_id = str(product_id)

        if product_id in self.basket:
            del self.basket[product_id]

        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        # remove basker from session
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def __iter__(self):
        """
        Collect the prodcut_id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids, is_active=True).prefetch_related('product_images')
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def __len__(self):
        """
        Get the basket data and count the quantity of items
        """
        return sum(item["qty"] for item in self.basket.values())

    def get_subtotal_price(self):
        subtotal = sum(
            Decimal(item["price"]) * item["qty"] for item in self.basket.values()
        )

        return subtotal

    def get_total_price(self):
        subtotal = self.get_subtotal_price()

        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(50.00)

        total = subtotal + shipping

        return total
