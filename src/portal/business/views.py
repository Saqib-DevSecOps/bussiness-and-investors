from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView

from src.accounts.decorators import business_required
from src.portal.business.models import Business, Project, Investor, Project_Investor, Shares


@method_decorator(business_required, name='dispatch')
class BusinessDashboard(TemplateView):
    template_name = 'business/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(BusinessDashboard, self).get_context_data(**kwargs)
        project = Project.objects.all()
        context['investor_count'] = Investor.objects.all().count()
        context['project_count'] = project.count()
        return context


@method_decorator(business_required, name='dispatch')
class ProjectListView(ListView):
    model = Project

    def get_queryset(self):
        user = self.request.user
        return Project.objects.select_related('business').filter(business__user=user)


@method_decorator(business_required, name='dispatch')
class ProjectCreateView(CreateView):
    model = Project
    fields = ['name', 'logo', 'category', 'website']
    success_url = reverse_lazy('business:dashboard')

    def form_valid(self, form):
        business = Business.objects.get(user=self.request.user)
        form.instance.business = business
        messages.success(self.request, 'Project Created Successfully')
        return super(ProjectCreateView, self).form_valid(form)


@method_decorator(business_required, name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['name', 'logo', 'category', 'website']
    success_url = reverse_lazy('business:dashboard')


@method_decorator(business_required, name='dispatch')
class ProjectDeleteView(DeleteView):
    template_name = 'business/project_delete.html'
    model = Project
    success_url = reverse_lazy('business:dashboard')

    def get_queryset(self):
        user = self.request.user
        return Project.objects.select_related('business').filter(business__user=user)


@method_decorator(business_required, name='dispatch')
class ProjectShareList(CreateView):
    model = Shares
    fields = ['status', 'value', 'percentage_equity']
    template_name = 'business/project_investor_create.html'
    success_url = reverse_lazy('business:project_list')

    def form_valid(self, form):
        project = Project.objects.get(id=self.kwargs['pk'])
        form.instance.project = project
        return super(ProjectShareList, self).form_valid(form)

@method_decorator(business_required, name='dispatch')
class ProjectShareUpdate(UpdateView):
    model = Shares
    fields = ['status', 'value', 'percentage_equity']
    template_name = 'business/project_investor_create.html'
    success_url = reverse_lazy('business:project_list')


@method_decorator(business_required, name='dispatch')
class ProjectShareDelete(DeleteView):
    model = Shares
    template_name = 'business/project_share_delete.html'
    success_url = reverse_lazy('business:project_list')


@method_decorator(business_required, name='dispatch')
class SharesListView(ListView):
    model = Shares
    template_name = 'business/shares_list.html'

    def get_queryset(self):
        return Shares.objects.filter(project_id=self.kwargs['pk'])
