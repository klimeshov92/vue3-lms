from django_filters import rest_framework as filters
from .models import *

class EventTemplateFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = EventTemplate
        fields = ['name', 'categories']

class EventSlotFilter(filters.FilterSet):
    planned_start = filters.DateTimeFilter(field_name='planned_start', lookup_expr='gte')
    planned_end = filters.DateTimeFilter(field_name='planned_end', lookup_expr='lte')

    class Meta:
        model = EventSlot
        fields = ['planned_start']




