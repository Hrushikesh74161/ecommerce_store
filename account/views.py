from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View, CreateView, DeleteView, UpdateView
from django.views.generic.edit import DeletionMixin

from account.forms import RegistrationForm, UserEditForm, UserAddressForm
from account.models import Customer, Address
from account.token import account_activation_token
from orders.views import user_orders
from store.models import Product
from account.decorators import redirect_if_authenticated


class AccountRegistration(FormView):
    form_class = RegistrationForm

    @method_decorator(redirect_if_authenticated)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs):
        register_form = self.get_form()
        return render(
            request, "account/registration/register.html", {"form": register_form}
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        register_form = self.get_form()
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


class AccountActivate(TemplateView):
    template_name = 'account/registration/acitvatin_invalid.html'

    def get(self, request, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(self.kwargs.get('uidb64')))
            user = Customer.objects.get(pk=uid)
        except:
            pass
        token = self.kwargs.get('token')
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('account:dashboard')
        else:
            return self.render_to_response({})


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'account/dashboard/dashboard.html'


class AllOrders(LoginRequiredMixin, ListView):
    template_name = 'account/dashboard/all_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return user_orders(self.request)


class EditDetails(LoginRequiredMixin, FormView):
    form_class = UserEditForm
    template_name = 'account/dashboard/edit_details.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.request.user})
        return kwargs

    def get(self, request, *args, **kwargs):
        user_form = self.get_form()
        return self.render_to_response({'user_form': user_form})

    def post(self, request, *args, **kwargs):
        user_form = self.get_form()
        if user_form.is_valid():
            user_form.save()
        return self.render_to_response({'user_form': user_form})


class DeleteUser(LoginRequiredMixin, DeletionMixin, View):
    success_url = reverse_lazy('account:delete_confirmation')

    def get_object(self):
        return self.request.user

    def delete(self, request: HttpRequest, *args: str, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        logout(request)
        return HttpResponseRedirect(success_url)


class ViewAddresses(LoginRequiredMixin, ListView):
    template_name = 'account/dashboard/addresses.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        addresses = Address.objects.filter(customer=self.request.user)
        return addresses


class AddAddress(LoginRequiredMixin, FormView):
    form_class = UserAddressForm
    template_name = 'account/dashboard/edit_addresses.html'
    
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form = form.save(commit=False)
            form.customer = request.user
            form.save()
            return redirect('account:addresses')


class EditAddress(LoginRequiredMixin, FormView):
    form_class = UserAddressForm
    template_name = 'account/dashboard/edit_addresses.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        instance = get_object_or_404(Address, pk=id, customer=self.request.user)
        kwargs.update({'instance': instance})
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect('account:addresses')

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response({'form': form})


class DeleteAddress(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('account:addresses')

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Address, pk=id, customer=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class SetDefaultAddress(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        Address.objects.filter(customer=request.user, default=True).update(default=False)
        id = self.kwargs.get('id')
        Address.objects.filter(pk=id, customer=request.user).update(default=True)
        return redirect("account:addresses")


class UserWishlist(LoginRequiredMixin, ListView):
    template_name = 'account/dashboard/user_wish_list.html'
    context_object_name = 'wishlist'

    def get_queryset(self):
        customer = Customer.objects.get(id=self.request.user.id)
        wishlist = customer.wishlist.all()
        return wishlist


class AddToWishlist(LoginRequiredMixin, View):
    
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Product, id=id)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if product.users_wishlist.filter(id=request.user.id).exists():
            product.users_wishlist.remove(request.user)
            messages.success(request, message=f"{product} removed from your wishlist.")
        else:
            product.users_wishlist.add(request.user)
            messages.success(request, message=f"{product} added to your wishlist.")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
