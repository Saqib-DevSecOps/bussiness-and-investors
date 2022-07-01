from django.urls import path, include

from . import views

app_name = 'business'

urlpatterns = [
    path('dashboard/', views.BusinessDashboard.as_view(), name='dashboard'),
    path('project-list/', views.ProjectListView.as_view(), name='project_list'),
    path('project-list/', views.ProjectListView.as_view(), name='project_list'),
    path('project-create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('project-update/<str:pk>/', views.ProjectCreateView.as_view(), name='project_create'),


]
