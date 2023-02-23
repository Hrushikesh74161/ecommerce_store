from django.urls import path

from store import views

app_name = "store"


urlpatterns = [
    path("", views.product_all, name="store_home"),
    path("item/<slug:slug>/", views.product_detail, name="product_detail"),
    path("search/<slug:category_slug>/", views.category_list, name="category_list"),
]