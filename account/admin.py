from django.contrib import admin

from account.models import Customer, Address


class AddressInline(admin.StackedInline):
    model = Address


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline,
    ]
