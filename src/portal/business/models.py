from django.db import models

# Create your models here.
from src.accounts.models import User


class Category(models.Model):
    title = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


filling_status = (
    ('True', u'Yes'),
    ('False', u'No')
)


class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='business/profile/')
    website = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=False)
    cro = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=200)
    registration_date = models.DateTimeField(null=True, blank=False)
    mandatory_filling = models.CharField(choices=filling_status, max_length=20)
    phone_no = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name


class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='investor/profiles')
    nationality = models.CharField(max_length=200)
    id_card = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='projects/')
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    cro = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=200)
    registration_date = models.DateTimeField(null=True, blank=False)
    website = models.CharField(max_length=120, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Shares(models.Model):
    choices = (
        ('equity', 'Equity'),)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(choices=choices, max_length=20, default='equity')
    value = models.PositiveIntegerField(default=0)
    percentage_equity = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    sell_equity = models.IntegerField(default=0)

    def __str__(self):
        return self.status


class Project_Investor(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    share = models.ForeignKey(Shares, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0)
    percentage_equity = models.DecimalField(max_digits=4,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.investor.user.username}'


class Payment(models.Model):
    payment_id = models.IntegerField()
    project_investor = models.ForeignKey(Project_Investor, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField()

    def __str__(self):
        return self.payment_id


class MoneyFlow(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    project_investor = models.ForeignKey(Project_Investor, on_delete=models.CASCADE, null=True, blank=True)
    business_profit_project = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    business_loss_project = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    investor_profit = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    investor_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    monthly_cost = models.IntegerField(default=0)
    monthly_earning = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project.name
