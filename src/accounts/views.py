from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms import ModelForm

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic.base import View

from src.portal.business.models import Business,Investor


@method_decorator(login_required, name='dispatch')
class CrossAuth(View):
    def get(self, request):
        if not self.request.user.is_completed:
            return redirect('accounts:identification_check')
        if self.request.user.is_superuser:
            return redirect('admin/')
        if self.request.user.is_business:
            return redirect('business:dashboard')
        else:
            return redirect('investor:dashboard')


@method_decorator(login_required, name='dispatch')
class IdentificationCheck(View):
    def get(self, request):
        return render(request, template_name='accounts/identification_check.html')

    def post(self, request):
        user_type = self.request.POST.get('user_type', None)
        if user_type is not None:
            if user_type == '1':
                messages.success(request, 'Fill the information to Complete your Business Profile')
                return redirect('accounts:business_complete_zone')
            elif user_type == '2':
                messages.success(request, 'Fill the information to Complete your Investor Profile')
                return redirect('accounts:investor_complete_zone')
        else:
            messages.error(request, 'Select User Usertype')
            return redirect('accounts:identification_check')

@method_decorator(login_required, name='dispatch')
class BusinessUserConfirm(CreateView):
    model = Business
    fields = ['business_name',
              'category',
              'logo',
              'cro',
              'registration_number',
              'registration_date',
              'phone_no',
              'website',
              'mandatory_filling'
              ]
    template_name = 'accounts/business_confirm.html'
    context_object_name = 'form'
    success_url = reverse_lazy('accounts:cross_auth')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = True
        user = self.request.user
        user.is_business = True
        user.is_completed = True
        user.save()
        return super(BusinessUserConfirm, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class InvestorUserConfirm(CreateView):
    model = Investor
    fields = ['id_card',
              'nationality',
              'profile_pic',
              'phone_no'
              ]
    template_name = 'accounts/investor_confirm.html'
    context_object_name = 'form'
    success_url = reverse_lazy('accounts:cross_auth')

    def form_valid(self, form):
        form.instance.user = self.request.user
        user = self.request.user
        user.is_investor = True
        user.is_completed = True
        user.save()
        return super(InvestorUserConfirm, self).form_valid(form)


class UserProfileForm(ModelForm):
    class Meta:
        model = Business
        fields = [
            'logo', 'business_name', 'category', 'website', 'cro', 'registration_number', 'phone_no'
        ]

class InvestorProfileForm(ModelForm):
    class Meta:
        model = Investor
        fields = [
            'profile_pic', 'nationality', 'id_card', 'phone_no'
        ]
        
@method_decorator(login_required, name='dispatch')
class UserUpdateView(View):

    def get(self, request):
        instance = Business.objects.get(user=self.request.user)
        form = UserProfileForm(instance=instance)
        context = {'form': form}
        return render(request, template_name='accounts/user_update.html', context=context)

    def post(self, request):
        instance = Business.objects.get(user=request.user)
        form = UserProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            messages.success(request, "Your profile updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='accounts/user_update.html', context=context)


@method_decorator(login_required, name='dispatch')
class InvestorUpdateView(View):

    def get(self, request):
        instance = Investor.objects.get(user=self.request.user)
        form = InvestorProfileForm(instance=instance)
        context = {'form': form}
        return render(request, template_name='accounts/user_update.html', context=context)

    def post(self, request):
        instance = Investor.objects.get(user=request.user)
        form = InvestorProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            messages.success(request, "Your profile updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='accounts/investor_update.html', context=context)