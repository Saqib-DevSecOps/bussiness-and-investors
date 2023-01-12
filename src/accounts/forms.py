import random

from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from src.accounts.models import User
from src.portal.business.models import Business


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','username']



