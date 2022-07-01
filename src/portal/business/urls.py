from django.urls import path, include

from . import views

app_name = 'business'

urlpatterns = [
    path('dashboard/', views.BusinessDashboard.as_view(), name='dashboard'),
    path('project-list/', views.ProjectListView.as_view(), name='project_list'),
    path('project-list/', views.ProjectListView.as_view(), name='project_list'),
    path('project-create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('project-update/<str:pk>/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('project-delete/<str:pk>/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<str:pk>/shares/', views.ProjectShareList.as_view(), name='investor_shares'),
    path('project-Shares-list/<str:pk>/', views.SharesListView.as_view(), name='shares'),
    path('project-shares-update/<str:pk>/<str:project>/', views.ProjectShareUpdate.as_view(), name='shares_update'),
    path('project-share-delete/<str:pk>/<str:project>/', views.ProjectShareDelete.as_view(), name='shares_delete'),

]
