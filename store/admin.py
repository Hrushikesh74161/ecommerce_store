from django.contrib import admin
from django import forms
from mptt.admin import MPTTModelAdmin

from store.models import (
    Category,
    Product,
    ProductImage,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',),
    }
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]
