from django.shortcuts import get_object_or_404, render

from store.models import Category, Product


def product_all(request):
    products = Product.objects.prefetch_related('product_images').filter(is_active=True)
    return render(request, "store/index.html", {"products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "store/single.html", {"product": product})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug).get_descendants(include_self=True)
    products = Product.objects.prefetch_related('product_images').filter(
        category__in=category)
    return render(
        request, "store/category.html", {"category": category, "products": products}
    )
