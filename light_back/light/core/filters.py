from django_filters import rest_framework as filters
from .models import *
from django.contrib.auth.models import Permission

class AccountFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='username', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    is_active = filters.BooleanFilter(field_name='is_active')
    self_registration = filters.BooleanFilter(field_name='self_registration')
    user_permissions = filters.ModelMultipleChoiceFilter(
        field_name='user_permissions',
        queryset=Permission.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Account
        fields = ['username', 'email', 'last_name', 'is_active', 'self_registration', 'user_permissions']

class PermissionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Permission
        fields = ['name']

class ClientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Client
        fields = ['name', 'categories']

class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    parent_category = filters.ModelChoiceFilter(
        field_name='parent_category',
        queryset=Category.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Category
        fields = ['name', 'parent_category']

class AccountGroupFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    type = filters.ChoiceFilter(
        field_name='type',
        choices=AccountsGroup.TYPES,
        lookup_expr='exact',
    )
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='id'
    )
    user_set = filters.ModelMultipleChoiceFilter(
        field_name='user',
        queryset=Account.objects.all(),
        to_field_name='id'
    )
    permissions = filters.ModelMultipleChoiceFilter(
        field_name='permissions',
        queryset=Permission.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = AccountsGroup
        fields = ['name', 'type', 'categories', 'user_set', 'permissions']

class OrganizationFilter(filters.FilterSet):
    legal_name = filters.CharFilter(field_name='legal_name', lookup_expr='icontains')
    tin = filters.NumberFilter(field_name='tin', lookup_expr='icontains')

    class Meta:
        model = Organization
        fields = ['legal_name', 'tin']

class SubdivisionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    organization = filters.ModelChoiceFilter(
        field_name='organization',
        queryset=Organization.objects.all(),
        to_field_name='id'
    )
    parent_subdivision = filters.ModelChoiceFilter(
        field_name='parent_subdivision',
        queryset=Subdivision.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Subdivision
        fields = ['name', 'organization', 'parent_subdivision']

class PositionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    subdivision = filters.ModelChoiceFilter(
        field_name='subdivision',
        queryset=Subdivision.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Position
        fields = ['name', 'subdivision']

