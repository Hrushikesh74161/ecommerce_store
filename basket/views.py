from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, View, TemplateView

from basket.basket import Basket
from store.models import Product


class BasketSummary(TemplateView):
    # Instead of using ListView with custom get_queryset method
    # which returns Basket(self.request)
    # we are using TemplateView, and basket object required for
    # template is provided by our custom context processor
    template_name = "basket/summary.html"


class BaksetAdd(View):
    def post(self, request, *args, **kwargs):
        basket = Basket(self.request)
        if self.request.POST.get("action") == "post":
            # getting product and product request data
            product_id = int(request.POST.get("productid"))
            product_qty = int(request.POST.get("productqty"))
            product = get_object_or_404(Product, id=product_id)
            # adding product to session
            basket.add(product=product, qty=product_qty)
            # getting no of items in basket and returning it
            basket_qty = len(basket)
            response = JsonResponse({"qty": basket_qty})

            return response


class BasketDelete(View):
    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        if request.POST.get("action") == "post":
            product_id = int(request.POST.get("productid"))
            basket.delete(product_id=product_id)
            basket_subtotal = basket.get_subtotal_price()
            basket_total = basket.get_total_price()
            basket_qty = len(basket)
            response = JsonResponse(
                {"total": basket_total, "subtotal": basket_subtotal, "qty": basket_qty}
            )
            return response


class BasketUpdate(View):
    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        if request.POST.get("action") == "post":
            product_id = int(request.POST.get("productid"))
            product_qty = int(request.POST.get("productqty"))
            basket.update(product_id, product_qty)
            basket_subtotal = basket.get_subtotal_price()
            basket_total = basket.get_total_price()
            basket_qty = len(basket)
            response = JsonResponse(
                {"subtotal": basket_subtotal, "qty": basket_qty, "total": basket_total}
            )
            return response
