from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from store.models import Category, Product


class AllProducts(ListView):
    context_object_name = "products"
    template_name = "store/index.html"

    def get_queryset(self):
        return (
            Product.objects.prefetch_related("product_images")
            .filter(is_active=True)
            .only("title", "regular_price")
        )


class ProductDetail(DetailView):
    context_object_name = "product"
    model = Product
    template_name = "store/single.html"

    def get_object(self):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(self.model, slug=slug, is_active=True)


class CategoryList(ListView):
    template_name = "store/category.html"
    context_object_name = "products"

    def get(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category, slug=self.kwargs.get("category_slug")
        ).get_descendants(include_self=True)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        products = Product.objects.prefetch_related("product_images").filter(
            category__in=self.category
        )
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"category": self.category})
        return context
