from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def business_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='accounts/login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_business,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def investor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='accounts/login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_investor and u.is_active,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return function


def identification_check(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account/login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_completed,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
