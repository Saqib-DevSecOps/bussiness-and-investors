from django.contrib import messages
from django.forms import ModelForm
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import View

from src.accounts.decorators import business_required
from src.portal.business.models import Business, Project, Investor, Project_Investor, Shares


@method_decorator(business_required, name='dispatch')
class BusinessDashboard(TemplateView):
    template_name = 'business/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(BusinessDashboard, self).get_context_data(**kwargs)
        project = Project.objects.filter(business__user = self.request.user)
        context['investor_count'] = Investor.objects.all().count()
        context['project_count'] = project.count()
        context['project_investor'] = Project_Investor.objects.filter(share__project__business__user=self.request.user).\
            order_by('created_at').all()[:5]
        context['projects'] = Project.objects.filter(business__user = self.request.user).all()[:5]
        return context


@method_decorator(business_required, name='dispatch')
class ProjectListView(ListView):
    model = Project

    def get_queryset(self):
        user = self.request.user
        return Project.objects.select_related('business').filter(business__user=user)


@method_decorator(business_required, name='dispatch')
class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'object'
    template_name = 'business/project_detail.html'

    def get_queryset(self):
        user = self.request.user
        return Project.objects.select_related('business').filter(business__user=user)


@method_decorator(business_required, name='dispatch')
class ProjectCreateView(CreateView):
    model = Project
    fields = ['name', 'logo', 'category', 'website','cro','registration_number']
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


class ProjectShareForm(ModelForm):
    class Meta:
        model = Shares
        fields = ['status', 'value', 'percentage_equity']


@method_decorator(business_required, name='dispatch')
class ProjectShareView(View):
    def get(self, request, pk):
        form = ProjectShareForm
        context = {'form': form}
        return render(request, 'business/project_investor_create.html', context)

    def post(self, request, pk):
        user_value = request.POST.get('value')
        percentage_equ = request.POST.get('percentage_equity')
        project = Project.objects.get(id=pk)
        project_share, created = Shares.objects.get_or_create(
            project=project
        )
        project_share.value = int(project_share.value) + int(user_value)
        project_share.percentage_equity = float(project_share.percentage_equity) + float(percentage_equ)
        project_share.save()
        messages.success(request, f'You request For Selling Share is Posted')
        return redirect('business:project_list')


# @method_decorator(business_required, name='dispatch')
# class ProjectShareCreate(CreateView):
#     model = Shares
#     fields = ['status', 'value', 'percentage_equity']
#     template_name = 'business/project_investor_create.html'
#     success_url = reverse_lazy('business:project_list')
#
#     def form_valid(self, form):
#         project = Project.objects.get(id=self.kwargs['pk'])
#         form.instance.project = project
#         return super(ProjectShareCreate, self).form_valid(form)


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
        return Shares.objects.filter(project__business__user=self.request.user)


#
@method_decorator(business_required, name='dispatch')
class ShareInvestors(ListView):
    model = Project_Investor
    template_name = 'business/project_investor.html'

    def get_queryset(self):
        return Project_Investor.objects.filter(share__project__business__user=self.request.user)


class ShareInvestorDetailView(DetailView):
    model = Project_Investor
    context_object_name = 'object'
    template_name = 'business/investor_Detail.html'

    def get_context_data(self, **kwargs):
        context = super(ShareInvestorDetailView, self).get_context_data(**kwargs)
        investor = Investor.objects.filter(id=self.kwargs['pk'])
        project_share = Project_Investor.objects.filter(investor=investor)
        context['projects'] = project_share
        return context