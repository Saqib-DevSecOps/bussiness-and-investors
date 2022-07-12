from decimal import Decimal

from django.contrib import messages
from django.core.paginator import Paginator
from django.forms import ModelForm
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import View

from src.accounts.decorators import business_required
from src.portal.business.bll import money_flow
from src.portal.business.filter import ProjectFilter
from src.portal.business.models import Business, Project, Investor, Project_Investor, Shares, MoneyFlow


@method_decorator(business_required, name='dispatch')
class BusinessDashboard(TemplateView):
    template_name = 'business/dashboard.html'

    def get_context_data(self, **kwargs):
        business_profit_project, business_loss_project, investor_profit, investor_loss = money_flow(self,
                                                                                                    request=self.request)
        context = super(BusinessDashboard, self).get_context_data(**kwargs)
        project = Project.objects.filter(business__user=self.request.user)
        context['investor_count'] = Investor.objects.all().count()
        context['project_count'] = project.count()
        context['project_investor'] = Project_Investor.objects.filter(share__project__business__user=self.request.user). \
                                          order_by('created_at').all()[:5]
        context['Buy_Shares'] = Project_Investor.objects.filter(share__project__business__user=self.request.user). \
            order_by('created_at').all()[:5].count()
        context['projects'] = Project.objects.filter(business__user=self.request.user).all()[:5]
        context['business_profit'] = business_profit_project
        context['business_loss'] = business_loss_project
        context['investor_profit'] = investor_profit
        context['investor_loss'] = investor_loss
        return context


@method_decorator(business_required, name='dispatch')
class ProjectListView(ListView):
    model = Project
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        user = self.request.user
        object_list = Project.objects.select_related('business').filter(business__user=user)
        filter_form = ProjectFilter(self.request.GET, object_list)
        paginator = Paginator(filter_form.qs,5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['form'] = filter_form.form
        context['object_list'] = page_obj
        return context


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
    fields = ['name', 'logo', 'category', 'website', 'cro', 'registration_number']
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


class MoneyFLowForm(ModelForm):
    class Meta:
        model = MoneyFlow
        fields = ['monthly_cost', 'monthly_earning']


@method_decorator(business_required, name='dispatch')
class MoneyFLowView(View):
    def get(self, request, pk):
        form = MoneyFLowForm
        context = {'form': form}
        return render(request, 'business/moneyflow.html', context)

    def post(self, request, pk):
        project = Project.objects.get(id=pk)
        project_investor = Project_Investor.objects.filter(share__project=project).first()
        cost = int(request.POST.get('cost'))
        earning = int(request.POST.get('earning'))
        if project_investor:
            money_flow, created = MoneyFlow.objects.get_or_create(project=project, project_investor=project_investor)
            investor_equity = Decimal(project_investor.percentage_equity)
            if int(earning) >= int(cost):
                profit = Decimal(earning) - Decimal(cost)

                print("Profit ", profit)
                money_flow.business_profit_project = (Decimal(profit) / Decimal(earning)) * 100
                print("business ", money_flow.business_profit_project)
                money_flow.business_loss_project = 0
                money_flow.investor_loss = 0
                inves_profit = (Decimal(investor_equity) * Decimal(earning)) / 100
                print("invest ", inves_profit)
                money_flow.investor_profit = Decimal(inves_profit) / Decimal(earning) * 100
                print("invest_prof ", money_flow.investor_profit)
                money_flow.monthly_cost = int(cost)
                money_flow.monthly_earning = int(earning)
                print("earning ", earning)
            elif int(earning) <= int(cost):
                profit = Decimal(cost) - Decimal(earning)
                money_flow.business_profit_project = 0
                money_flow.investor_profit = 0
                money_flow.business_loss_project = (Decimal(profit) / Decimal(cost)) * 100
                inves_profit = (Decimal(investor_equity) * Decimal(earning)) / 100
                money_flow.investor_loss = (Decimal(inves_profit) / Decimal(earning)) * 100
                money_flow.monthly_cost = int(cost)
                money_flow.monthly_earning = int(earning)
            money_flow.save()
            return redirect('business:project_list')
        else:
            money_flow, created = MoneyFlow.objects.get_or_create(project=project)
            if int(earning) >= int(cost):
                profit = Decimal(earning) - Decimal(cost)
                money_flow.business_profit_project = (Decimal(profit) / Decimal(earning)) * 100
                money_flow.business_loss_project = 0
                money_flow.monthly_cost = int(cost)
                money_flow.monthly_earning = int(earning)
            elif int(earning) <= int(cost):
                profit = Decimal(cost) - Decimal(earning)
                money_flow.business_loss_project = (Decimal(profit) / Decimal(cost)) * 100
                money_flow.business_profit_project = 0
                money_flow.monthly_cost = int(cost)
                money_flow.monthly_earning = int(earning)
            money_flow.save()
            return redirect('business:project_list')
