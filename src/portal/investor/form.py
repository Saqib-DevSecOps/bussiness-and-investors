from django.forms import ModelForm
from django import forms
from src.portal.business.models import Project_Investor
class BuyShareForm(ModelForm):
    class Meta:
        model = Project_Investor
        fields = ['value','is_agree']
        widgets = {
            'is_agree' : forms.CheckboxInput(attrs={'class': 'required checkbox form-check','id': 'checkbox'}),   
        }
        

class SellShareForm(ModelForm):
    class Meta:
        model = Project_Investor
        fields = ['value','percentage_equity']
