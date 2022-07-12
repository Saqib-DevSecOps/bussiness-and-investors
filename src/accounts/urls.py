from django.urls import path, include

from src.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('cross-auth/', views.CrossAuth.as_view(), name='cross_auth'),
    path('identification/', views.IdentificationCheck.as_view(), name='identification_check'),
    path('business-confirmation/', views.BusinessUserConfirm.as_view(), name='business_complete_zone'),
    path('investor-confirmation/', views.InvestorUserConfirm.as_view(), name='investor_complete_zone'),
    path('update_profile/', views.UserUpdateView.as_view(), name='update_profile'),
    path('investor_update_profile/', views.InvestorUpdateView.as_view(), name='investor_update_profile'),

]
