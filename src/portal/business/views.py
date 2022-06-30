from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from src.accounts.decorators import business_required
from src.portal.business.models import Business

@method_decorator(business_required, name='dispatch')
class BusinessDashboard(ListView):
    model = Business
    template_name = 'business/dashboard.html'
