from django.urls import path

from basket import views

app_name = "basket"

urlpatterns = [
    path("", views.BasketSummary.as_view(), name="basket_summary"),
    path("add/", views.BaksetAdd.as_view(), name="basket_add"),
    path("delete/", views.BasketDelete.as_view(), name="basket_delete"),
    path("update/", views.BasketUpdate.as_view(), name="basket_update"),
]
