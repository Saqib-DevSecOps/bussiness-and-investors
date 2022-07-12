
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render,redirect


# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View,ListView, TemplateView, CreateView, UpdateView, DetailView
from . form import BuyShareForm, SellShareForm
from src.accounts.decorators import investor_required
from src.portal.business.models import Business, Project, Investor, Shares, Project_Investor,InvestorShare
from src.portal.investor.bll import money_flow
from ..business.filter import ProjectFilter, ProjectShareFilter


@method_decorator(investor_required, name='dispatch')
class InvestorDashboard(TemplateView):
    template_name = 'investor/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(InvestorDashboard, self).get_context_data(**kwargs)
        project = Project.objects.all()
        share = Shares.objects.all()
        business_profit_project, business_loss_project, investor_profit, investor_loss = money_flow(self,request=self.request)


        project_investor=Project_Investor.objects.all()
        context['applied_project'] = project_investor.count()
        context['project_count'] = project.count()
        context['project_list'] = Project.objects.all()
        
        context['investor_profit'] = investor_profit

        context['object_list'] = Project_Investor.objects.filter(investor__user=self.request.user,value__gt=0).all()[:10]
        return context




@method_decorator(investor_required, name='dispatch')
class ProjectListView(ListView):
    model = Shares
    template_name = 'investor/project_list.html'

    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        object_list = Shares.objects.filter(value__gt=0)
        filter_form = ProjectShareFilter(self.request.GET, object_list)
        context['form'] = filter_form.form
        context['object_list'] = filter_form.qs
        return context





@method_decorator(investor_required, name='dispatch')
class BuyShareView(View):
    def get(self,request,pk,*args,**kwargs):
        form = BuyShareForm
        return render(request,'investor/buy_share.html')

    def post(self,request,pk,*args,**kwargs):

        # GET: required values
        form = BuyShareForm(request.POST)
        user_value = self.request.POST.get('value')
        # GET: share model values
        share = Shares.objects.get(id=pk)
        share_equity=share.percentage_equity
        share_value=share.value
        # CAL1: user calculations
        user_percentage=(int(user_value)/share_value)*100
        user_equity=(float(user_percentage)*float(share_equity))/100
        # user = request.user
        # user.value=user_value
        # user.percentage_equity=user_equity
        # user.save()
        # CAL2: project calculations
        user = request.user
        investor = Investor.objects.get(user = self.request.user)
        # project_inv = Project_Investor(
        #     investor=investor, share=share, value=user_value
        # )
        if int(user_value) <= int(share.value):
            project_investor,create = Project_Investor.objects.get_or_create(share=share,investor=investor)
            project_investor.value = int(user_value) + int(project_investor.value)
            project_investor.percentage_equity = float(project_investor.percentage_equity) + float(user_equity)
            project_investor.save()
            # project_inv.save()
            share.value=int(share_value)-int(user_value)
            share.percentage_equity=float(share_equity)-float(user_equity)
            share.sell_equity = float(share.sell_equity) + float(user_equity)
            share.save()
            return redirect('investor:dashboard')
        else:
            messages.error(request,'Enter a value less than or equall to')
            return redirect('investor:buy_share', pk)





@method_decorator(investor_required, name='dispatch')
class ShareDetailView(ListView):
    model = Project_Investor
    template_name = 'investor/share_detail.html' 

    def get_context_data(self, **kwargs):
        context = super(ShareDetailView, self).get_context_data(**kwargs)
        context['object_list'] = Project_Investor.objects.filter(investor__user=self.request.user)
        return context

@method_decorator(investor_required, name='dispatch')
class ViewShareDetail(DetailView):
    model = Project_Investor
    template_name = 'investor/share_view_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ViewShareDetail, self).get_context_data(**kwargs)
        p_i = self.get_object()
        return context


@method_decorator(investor_required, name='dispatch')
class SellShareView(View):

    def get(self,request,pk,*args,**kwargs):
        form = SellShareForm
        return render(request,'investor/sell_share.html')

    def post(self,request,pk,*args,**kwargs):

        # GET: required values
        form = SellShareForm(request.POST)
        user_value = self.request.POST.get('value')
        user_equity = self.request.POST.get('percentage')

        # GET: share model values
        share = Project_Investor.objects.get(id=pk)
        investor_share_equity=share.percentage_equity
        investor_share_value=share.value
        # CAL1: user calculations
        user_percentage=(int(user_value)/investor_share_value)*100
        user_equity=(float(user_equity)*float(investor_share_equity))/100

        if int(user_value) <= int(share.value):
            project_investor,created = InvestorShare.objects.get_or_create(project_investor = share)
            project_investor.value = int(project_investor.value) + int(user_value)
            project_investor.percentage_equity = int(project_investor.percentage_equity) + int(user_equity)
            project_investor.save()

            # project_inv.save()
            share.value=int(investor_share_value)-int(user_value)
            share.percentage_equity=float(investor_share_equity)-float(user_equity)
            share.save()

            return redirect('investor:dashboard')
        else:
            messages.error(request,'Enter a value less than or equall to')
            return redirect('investor:sell_share', pk)


@method_decorator(investor_required, name='dispatch')
class ProjectInvestorDetailView(DetailView):
    model = Project
    context_object_name = 'object'
    template_name = 'investor/project_detail.html'
    


class CompanyDetailView(DetailView):
    model = Project_Investor
    context_object_name = 'object'
    template_name = 'investor/company_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        business = Business.objects.filter(id=self.kwargs['pk'])
        context['projects'] = business
        return context

