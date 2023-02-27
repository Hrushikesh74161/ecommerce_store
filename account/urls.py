from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from account import views
from account.forms import PwdResetConfirmForm, PwdResetForm, UserLoginForm

app_name = "account"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="account/login.html", form_class=UserLoginForm
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/account/login/"),
        name="logout",
    ),
    path("register/", views.AccountRegistration.as_view(), name="register"),
    # path(
    #     "acitvate/<slug:uidb64>/<slug:token>/", views.account_activate, name="activate"
    # ),
    path(
        "acitvate/<slug:uidb64>/<slug:token>/",
        views.AccountActivate.as_view(),
        name="activate",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password_reset/password_reset_form.html",
            success_url="password_reset_email_confirm",
            email_template_name="account/password_reset/password_reset_email.html",
            form_class=PwdResetForm,
        ),
        name="pwdreset",
    ),
    path(
        "password_reset/password_reset_email_confirm/",
        TemplateView.as_view(template_name="account/password_reset/reset_status.html"),
        name="password_reset_email_confirm",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset/password_reset_confirm.html",
            success_url="/account/password_reset_complete/",
            form_class=PwdResetConfirmForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        TemplateView.as_view(template_name="account/password_reset/reset_status.html"),
        name="password_reset_complete",
    ),
    # User dashboard
    path("dashboard/", views.Dashboard.as_view(), name="dashboard"),
    path("dashboard/orders/", views.AllOrders.as_view(), name="all_orders"),
    path("profile/edit/", views.EditDetails.as_view(), name="edit_details"),
    path("profile/delete_user/", views.DeleteUser.as_view(), name="delete_user"),
    path(
        "profile/delete_confirm",
        TemplateView.as_view(template_name="account/dashboard/delete_confirm.html"),
        name="delete_confirmation",
    ),
    path("addresses/", views.ViewAddresses.as_view(), name="addresses"),
    path("add_address/", views.AddAddress.as_view(), name="add_address"),
    path("addresses/edit/<slug:id>/", views.EditAddress.as_view(), name="edit_address"),
    path(
        "addresses/delete/<slug:id>/",
        views.DeleteAddress.as_view(),
        name="delete_address",
    ),
    path(
        "addresses/set_default/<slug:id>/",
        views.SetDefaultAddress.as_view(),
        name="set_default_address",
    ),
    # wishlist
    path("wishlist/", views.UserWishlist.as_view(), name="wishlist"),
    path(
        "wishlist/add_to_wishlist/<int:id>",
        views.AddToWishlist.as_view(),
        name="add_to_wishlist",
    ),
]
