from django.urls import path, include

from . import views
from .views import SuccessPayment, CancelPayment

app_name = 'investor'

urlpatterns = [
    path('dashboard/', views.InvestorDashboard.as_view(), name='dashboard'),
    path('project-list/',views.ProjectListView.as_view(), name='project_list'),
    path('buy-share/<str:pk>/',views.BuyShareView.as_view(), name='buy_share'),
    path('view-share/<str:pk>/',views.ViewShareDetail.as_view(), name='view_share'),
    path('share_detail/',views.ShareDetailView.as_view(), name='share_detail'),
    path('project/<str:pk>/shares/', views.SellShareView.as_view(), name='investor_shares'),
    path('company-detail/<str:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('project-detail/<str:pk>/', views.ProjectInvestorDetailView.as_view(), name='project_detail'),
    path('payment-success/', SuccessPayment.as_view(), name="success"),
    path('payment-cancelled/', CancelPayment.as_view(), name="cancel"),


    

]
