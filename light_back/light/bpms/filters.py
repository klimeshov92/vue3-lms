from django_filters import rest_framework as filters
from .models import *
from core.models import *
from django.contrib.auth.models import Permission

class InteractionFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Interaction
        fields = ['id', 'categories']

class TaskTemplateFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )
    task_type = filters.MultipleChoiceFilter(
        field_name='task_type',
        choices=TaskTemplate.TASK_TYPES
    )

    class Meta:
        model = TaskTemplate
        fields = ['name', 'categories']

class TaskFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Task
        fields = ['name', 'categories']

class PublicTaskFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = PublicTask
        fields = ['name', 'categories']

class PublicPlanFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = PublicPlan
        fields = ['name', 'categories']

class TaskTemplateAssignmentFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = TaskTemplateAssignment
        fields = ['name', 'categories']

class QueueFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Queue
        fields = ['name', 'categories']

class ControlElementFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = ControlElement
        fields = ['name', 'categories']

