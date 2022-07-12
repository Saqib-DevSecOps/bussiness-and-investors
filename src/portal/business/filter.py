import django_filters
from django.db.models import Q
from django.forms import TextInput

from src.portal.business.models import Project, Category, Business, Shares


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='Name', widget=TextInput(attrs={'placeholder': 'Search Project By '
                                                                                          'Name / Cro / Registration '
                                                                                          'Number'}),
                                     method='my_custom_filter')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(),empty_label = 'Select Category')

    class Meta:
        model = Project
        fields = [
            'name',
            'category',
        ]

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(cro__icontains=value) | Q(registration_number__icontains=value) | Q(name__icontains=value))

class ProjectShareFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='Name', widget=TextInput(attrs={'placeholder': 'Search Project By '
                                                                                          'Name / Cro / Registration '
                                                                                          'Number'}),
                                     method='search_project')
    # category = django_filters.ModelChoiceFilter(queryset=Category.objects.filter(Category.project_set.project_id == Project.shared_project.project_id ),empty_label = 'Select Category',)

    class Meta:
        model = Shares
        fields = [
            'name',
        ]

    def search_project(self, queryset, name, value):
        return queryset.filter(
            Q(project__name__icontains=value) | Q(project__registration_number__icontains=value)
            | Q(project__cro__icontains=value))
