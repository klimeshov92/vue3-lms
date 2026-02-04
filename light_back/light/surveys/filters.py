from django_filters import rest_framework as filters
from .models import *

class SurveyFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Survey
        fields = ['name', 'categories']

class SurveyQuestionFilter(filters.FilterSet):
    text = filters.CharFilter(field_name='text', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = SurveyQuestion
        fields = ['text', 'categories']


