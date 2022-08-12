
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from .utils import isFirebaseAuthenticated


def unverified_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.customer.verified:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('sms-verification')
    return wrapper_func


def isAuthenticated(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = isFirebaseAuthenticated(request.session.get('uid'))
        if user:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('store')
    return wrapper_func
