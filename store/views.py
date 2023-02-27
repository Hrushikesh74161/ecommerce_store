from functools import lru_cache

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from store.models import Category, Product


class AllProducts(ListView):
    context_object_name = 'products'
    template_name = 'store/index.html'

    def get_queryset(self):
        return Product.objects.prefetch_related('product_images').filter(is_active=True)
    

class ProductDetail(DetailView):
    context_object_name = 'product'
    model = Product
    template_name = 'store/single.html'

    def get_object(self):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(self.model, slug=slug, is_active=True)


class CategoryList(ListView):
    template_name = 'store/category.html'

    @lru_cache
    def get_category(self):
        return get_object_or_404(Category, slug=self.kwargs.get('category_slug')).get_descendants(include_self=True)
    
    def get_queryset(self):
        products = Product.objects.prefetch_related('product_images').filter(
        category__in=self.get_category())
        return products

    def get_context_data(self):
        category = self.get_category()
        products = self.get_queryset()
        return {'category': category, 'products': products}
    