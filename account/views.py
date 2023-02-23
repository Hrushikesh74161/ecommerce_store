from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse

from account.forms import RegistrationForm, UserEditForm, UserAddressForm
from account.models import Customer, Address
from account.token import account_activation_token
from orders.views import user_orders
from store.models import Product


def account_register(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data["email"]
            user.set_password(register_form.cleaned_data["password"])
            user.is_active = False
            user.save()
            # setup email
            current_site = get_current_site(request)
            subject = "Activate your account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(
                request,
                "account/registration/register_email_confirm.html",
                {"form": register_form},
            )
    else:
        register_form = RegistrationForm()

    return render(
        request, "account/registration/register.html", {"form": register_form}
    )


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        render(request, "account/registration/activation_invalid.html")


@login_required
def dashboard(request):
    return render(request, "account/dashboard/dashboard.html")


@login_required
def all_orders(request):
    orders = user_orders(request)
    return render(request, "account/dashboard/all_orders.html", {"orders": orders})


@login_required
def edit_details(request: HttpRequest):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(
        request, "account/dashboard/edit_details.html", {"user_form": user_form}
    )


@login_required
def delete_user(request: HttpRequest):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")


@login_required
def view_addresses(request: HttpRequest):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request: HttpRequest):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(
        request, "account/dashboard/edit_addresses.html", {"form": address_form}
    )


@login_required
def edit_address(request: HttpRequest, id):
    address = get_object_or_404(Address, pk=id, customer=request.user)
    if request.method == "POST":
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm(instance=address)

    return render(
        request, "account/dashboard/edit_addresses.html", {"form": address_form}
    )


@login_required
def delete_address(request: HttpRequest, id):
    address = get_object_or_404(Address, pk=id, customer=request.user)
    address.delete()
    return redirect("account:addresses")


@login_required
def set_default_address(request: HttpRequest, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
    return redirect("account:addresses")


@login_required
def user_wishlist(request: HttpRequest):
    customer = Customer.objects.get(id=request.user.id)
    wishlist = customer.wishlist.all()
    return render(request, 'account/dashboard/user_wish_list.html', {'wishlist': wishlist})


@login_required
def add_to_wishlist(request: HttpRequest, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, message=f'{product} removed from your wishlist.')
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, message=f'{product} added to your wishlist.')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
