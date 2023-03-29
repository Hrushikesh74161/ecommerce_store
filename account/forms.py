from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)

from account.models import Customer, Address


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "full_name",
            "phone",
            "address_line1",
            "address_line2",
            "town_city",
            "postcode",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["full_name"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Full Name",
            },
        )

        self.fields["phone"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Phone",
            },
        )

        self.fields["address_line1"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Address Line 1",
            },
        )

        self.fields["address_line2"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Address Line 2",
            },
        )

        self.fields["town_city"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Town/City/State",
            },
        )

        self.fields["postcode"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Postcode",
            },
        )


class RegistrationForm(forms.ModelForm):
    name = forms.CharField(
        label="Enter Name",
        min_length=4,
        max_length=50,
        help_text="Required",
    )

    email = forms.EmailField(
        max_length=100,
        help_text="Required",
        error_messages={"required": "Sorry, you will need an email."},
    )

    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    password2 = forms.CharField(
        label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = (
            "name",
            "email",
        )

    def clean_name(self):
        name = self.cleaned_data["name"].lower()
        r = Customer.objects.filter(name=name)
        if r.count():
            raise forms.ValidationError("Name already exists.")
        return name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Account already exists with that email.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "name"}
        )
        self.fields["email"].widget.attrs.update({
            "class": "form-control mb-3",
            "placeholder": "email",
            "name": "email"
        })
        self.fields["password"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Repeat password"}
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "id": "login-username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "login-pwd",
            }
        )
    )


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label="Account email (can not be changed)",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "email",
                "id": "form-email",
                "readonly": "readonly",
            }
        ),
    )

    name = forms.CharField(
        label="Name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "paceholder": "Name",
                "id": "form-firstname",
            },
        ),
    )

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["email"].required = True


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "paceholder": "Email",
                "id": "form-email",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = Customer.objects.get(email=email)
        if not user:
            raise forms.ValidationError(
                "No account registered with that email.")
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "paceholder": "New Password",
                "id": "form-newpass",
            }
        ),
    )

    new_password2 = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "paceholder": "New Password",
                "id": "form-new-pass2",
            }
        ),
    )
