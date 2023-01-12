from django.contrib import admin
from .models import Business, Shares, Project, Project_Investor, Investor, Payment, Category, MoneyFlow

# Register your models here.

admin.site.register(Business)
admin.site.register(Shares)
admin.site.register(Project)
admin.site.register(Project_Investor)
admin.site.register(Investor)
admin.site.register(Category)
admin.site.register(Payment)
admin.site.register(MoneyFlow)
