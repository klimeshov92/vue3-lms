from django_filters import rest_framework as filters
from .models import *

class TestFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Test
        fields = ['name', 'categories']

class QuestionFilter(filters.FilterSet):
    text = filters.CharFilter(field_name='text', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Question
        fields = ['text', 'categories']


