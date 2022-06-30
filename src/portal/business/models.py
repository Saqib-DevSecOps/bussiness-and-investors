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
    mandatory_filling = models.CharField(choices=filling_status,max_length=20)
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
    website = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.name


class Shares(models.Model):
    choices = (
        ('sin', 'Single Owner'),
        ('shared', 'Shared Owner'),
    )
    equity = models.DecimalField(max_digits=4, decimal_places=2)
    owner = models.CharField(choices=choices, max_length=20)
    value = models.IntegerField()

    def __str__(self):
        return self.id


class Project_Investor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    share = models.ForeignKey(Shares, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.project.name}   {self.investor.user.username}'


class Payment(models.Model):
    payment_id = models.IntegerField()
    project_investor = models.ForeignKey(Project_Investor, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField()

    def __str__(self):
        return self.payment_id
