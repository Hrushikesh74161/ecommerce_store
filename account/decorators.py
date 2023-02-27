from django.http import HttpRequest
from django.shortcuts import redirect


def redirect_if_authenticated(func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return func(request, *args, **kwargs)

    return wrapper