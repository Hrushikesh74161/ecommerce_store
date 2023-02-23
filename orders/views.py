from django.http import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import render

from basket.basket import Basket
from orders.models import Order, OrderItem


def add(request: HttpRequest):
    basket = Basket(request)

    if request.POST.get("action") == "post":
        user_id = request.user.id
        order_key = request.POST.get("order_key")
        baskettotal = basket.get_total_price()

        # check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id=user_id,
                full_name="name",
                address1="add1",
                address2="add2",
                total_paid=baskettotal,
                order_key=order_key,
            )
            order_id = order.pk
            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["qty"],
                )
        response = JsonResponse({"success": "Order placed successfully"})
        return response


def payment_confirmation(client_secret):
    Order.objects.filter(order_key=client_secret).update(billing_status=True)


def user_orders(request: HttpRequest):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
