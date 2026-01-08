
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError
from django.apps import apps
from django.contrib.auth.models import User, Group
from notifications.models import NotificationSettings
from rest_framework import serializers
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

import logging
logger = logging.getLogger('project')


class AccountBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = '__all__'

    def get_str(self, obj):
        positions_subdivisions_organizations_list = [
            f"{placement.position.name} - {placement.position.subdivision.name} - {placement.position.subdivision.organization.legal_name}"
            for placement in obj.placements.filter(end_date=None)
        ]
        positions_subdivisions_organizations_str = ' | '.join(positions_subdivisions_organizations_list)
        if obj.last_name and obj.first_name and obj.placements.exists():
            return f'{obj.username} - {obj.last_name} {obj.first_name} - ({positions_subdivisions_organizations_str})'
        elif obj.last_name and obj.first_name:
            return f'{obj.username} - {obj.last_name} {obj.first_name}'
        else:
            return f'{obj.username}'

class ClientBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Client
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.name}'

class CategoryBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_str(self, obj):
        # Получение родительских категорий по цепочке.
        def get_parents_chain(obj):
            if obj.parent_category:
                return f'{obj.parent_category.get_parents_chain()} - {obj.name}'
            else:
                return obj.name

        return f'{obj.get_parents_chain()}'

class AccountsGroupBaseSerializer(serializers.ModelSerializer):
    user_set = AccountBaseSerializer(many=True, required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = AccountsGroup
        fields = '__all__'

    def get_str(self, obj):
        # Имя в зависимости от связанного объекта.
        if hasattr(obj, 'organization'):
            return f'{obj.name}'
        elif hasattr(obj, 'subdivision'):
            return f'{obj.name} - {obj.subdivision.organization.legal_name}'
        elif hasattr(obj, 'position'):
            return f'{obj.name} - {obj.position.subdivision.name} - {obj.position.subdivision.organization.legal_name}'
        else:
            return f'{obj.name}'

class ContentTypeBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()

    class Meta:
        model = ContentType
        fields = '__all__'

    def get_str(self, obj):
        model_class = apps.get_model(app_label=obj.app_label, model_name=obj.model)
        return model_class._meta.verbose_name_plural

class PermissionBaseSerializer(serializers.ModelSerializer):
    content_type = ContentTypeBaseSerializer()

    class Meta:
        model = Permission
        fields = '__all__'

class PermissionEditSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all(), required=False)

    class Meta:
        model = Permission
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)


class AccountsGroupObjectPermissionBaseSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    permission = PermissionBaseSerializer()
    content_type = ContentTypeBaseSerializer()
    content_object = serializers.StringRelatedField()
    group = AccountsGroupBaseSerializer()

    class Meta:
        model = AccountsGroupObjectPermission
        fields = '__all__'

class AccountObjectPermissionBaseSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    permission = PermissionBaseSerializer()
    content_type = ContentTypeBaseSerializer()
    content_object = serializers.StringRelatedField()
    user = AccountBaseSerializer()

    class Meta:
        model = AccountObjectPermission
        fields = '__all__'

class OrganizationBaseSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()
    group = AccountsGroupBaseSerializer()

    class Meta:
        model = Organization
        fields = '__all__'

class SubdivisionBaseSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()
    organization = OrganizationBaseSerializer()
    group = AccountsGroupBaseSerializer

    class Meta:
        model = Subdivision
        fields = '__all__'

class PositionBaseSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()
    subdivision = SubdivisionBaseSerializer()
    group = AccountsGroupBaseSerializer

    class Meta:
        model = Position
        fields = '__all__'

class PlacementBaseSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()
    account = AccountBaseSerializer()
    position = PositionBaseSerializer()

    class Meta:
        model = Placement
        fields = '__all__'

class GroupGeneratorBaseSerializer(serializers.ModelSerializer):
    group = AccountsGroupBaseSerializer(required=False)
    added_groups = AccountsGroupBaseSerializer(many=True, required=False)
    added_users = AccountBaseSerializer(many=True, required=False)
    excluded_groups = AccountsGroupBaseSerializer(many=True, required=False)
    excluded_users = AccountBaseSerializer(many=True, required=False)
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = GroupGenerator
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    user_permissions = PermissionBaseSerializer(many=True, required=False)
    groups = AccountsGroupBaseSerializer(many=True, required=False)
    placements = PlacementBaseSerializer(many=True, required=False)
    self_object_permissions = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    avatar = serializers.ImageField(required=False)
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = '__all__'

    def get_str(self, obj):
        positions_subdivisions_organizations_list = [
            f"{placement.position.name} - {placement.position.subdivision.name} - {placement.position.subdivision.organization.legal_name}"
            for placement in obj.placements.filter(end_date=None)
        ]
        positions_subdivisions_organizations_str = ' | '.join(positions_subdivisions_organizations_list)
        if obj.last_name and obj.first_name and obj.placements.exists():
            return f'{obj.username} - {obj.last_name} {obj.first_name} - ({positions_subdivisions_organizations_str})'
        elif obj.last_name and obj.first_name:
            return f'{obj.username} - {obj.last_name} {obj.first_name}'
        else:
            return f'{obj.username}'

    def get_self_object_permissions(self, obj):
        permissions = AccountObjectPermission.objects.filter(user=obj)
        return AccountObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_accounts_group_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountsGroupObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountsGroupObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_account_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

class CabinetNotificationSettingsSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()

    class Meta:
        model = NotificationSettings
        fields = '__all__'

    def get_str(self, obj):
        return f"{obj.account.username}"

class CabinetSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    user_permissions = PermissionBaseSerializer(many=True, required=False)
    groups = AccountsGroupBaseSerializer(many=True, required=False)
    placements = PlacementBaseSerializer(many=True, required=False)
    self_object_permissions = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    notification_settings = CabinetNotificationSettingsSerializer(required=False)
    avatar = serializers.ImageField(required=False)
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = '__all__'

    def get_str(self, obj):
        positions_subdivisions_organizations_list = [
            f"{placement.position.name} - {placement.position.subdivision.name} - {placement.position.subdivision.organization.legal_name}"
            for placement in obj.placements.filter(end_date=None)
        ]
        positions_subdivisions_organizations_str = ' | '.join(positions_subdivisions_organizations_list)
        if obj.last_name and obj.first_name and obj.placements.exists():
            return f'{obj.username} - {obj.last_name} {obj.first_name} - ({positions_subdivisions_organizations_str})'
        elif obj.last_name and obj.first_name:
            return f'{obj.username} - {obj.last_name} {obj.first_name}'
        else:
            return f'{obj.username}'

    def get_self_object_permissions(self, obj):
        permissions = AccountObjectPermission.objects.filter(user=obj)
        return AccountObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_accounts_group_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountsGroupObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountsGroupObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_account_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

class AccountEditSerializer(serializers.ModelSerializer):
    user_permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True, required=False)
    groups = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), many=True, required=False)
    placements = serializers.PrimaryKeyRelatedField(queryset=Placement.objects.all(), many=True, required=False)
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Account
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class CabinetEditSerializer(serializers.ModelSerializer):
    user_permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True, required=False)
    groups = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), many=True, required=False)
    placements = serializers.PrimaryKeyRelatedField(queryset=Placement.objects.all(), many=True, required=False)
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Account
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class ClientSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    account = AccountBaseSerializer(required=False)
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    categories = CategoryBaseSerializer(many=True, required=False)
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Client
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.name}'

    def get_accounts_group_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountsGroupObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountsGroupObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_account_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

class ClientEditSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), required=False, allow_null=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)

    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class PermissionSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    content_type = ContentTypeBaseSerializer()

    class Meta:
        model = Permission
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.content_type} - {obj.name}'

class CategorySerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    parent_category = CategoryBaseSerializer()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_str(self, obj):
        # Получение родительских категорий по цепочке.
        def get_parents_chain(obj):
            if obj.parent_category:
                return f'{obj.parent_category.get_parents_chain()} - {obj.name}'
            else:
                return obj.name

        return f'{obj.get_parents_chain()}'

    def get_accounts_group_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountsGroupObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountsGroupObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_account_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

class CategoryEditSerializer(serializers.ModelSerializer):
    parent_category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class AccountsGroupSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    type_display = serializers.SerializerMethodField()
    categories = CategoryBaseSerializer(many=True, required=False)
    user_set = AccountBaseSerializer(many=True, required=False)
    permissions = PermissionBaseSerializer(many=True, required=False)
    generator_group = GroupGeneratorBaseSerializer(required=False)
    self_object_permissions = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = AccountsGroup
        fields = '__all__'

    def get_str(self, obj):
        # Имя в зависимости от связанного объекта.
        if hasattr(obj, 'organization'):
            return f'{obj.name}'
        elif hasattr(obj, 'subdivision'):
            return f'{obj.name} - {obj.subdivision.organization.legal_name}'
        elif hasattr(obj, 'position'):
            return f'{obj.name} - {obj.position.subdivision.name} - {obj.position.subdivision.organization.legal_name}'
        else:
            return f'{obj.name}'

    def get_type_display(self, obj):
        return obj.get_type_display()

    def get_self_object_permissions(self, obj):
        permissions = AccountsGroupObjectPermission.objects.filter(group=obj)
        return AccountsGroupObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_accounts_group_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountsGroupObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountsGroupObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_account_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

class AccountsGroupEditSerializer(serializers.ModelSerializer):
    user_set = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), many=True, required=False)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True, required=False)

    class Meta:
        model = AccountsGroup
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class GroupGeneratorSerializer(serializers.ModelSerializer):
    group = AccountsGroupBaseSerializer(required=False)
    added_groups = AccountsGroupBaseSerializer(many=True, required=False)
    added_users = AccountBaseSerializer(many=True, required=False)
    excluded_groups = AccountsGroupBaseSerializer(many=True, required=False)
    excluded_users = AccountBaseSerializer(many=True, required=False)
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = GroupGenerator
        fields = '__all__'

class GroupGeneratorEditSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all())
    added_groups = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), many=True, required=False)
    added_users = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), many=True, required=False)
    excluded_groups = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), many=True, required=False)
    excluded_users = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), many=True, required=False)

    class Meta:
        model = GroupGenerator
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

    def validate_group(self, value):
        if value.type != 'custom':
            raise serializers.ValidationError("Группа должна быть пользовательской.")
        return value

class AccountsGroupObjectPermissionEditSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all())
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all(), required=False)
    # object_pk
    permission = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), required=False)

    class Meta:
        model = AccountsGroupObjectPermission
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

class AccountObjectPermissionEditSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all(), required=False)
    # object_pk
    permission = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), required=False)

    class Meta:
        model = AccountObjectPermission
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

class OrganizationSerializer(serializers.ModelSerializer):
    group = AccountsGroupBaseSerializer()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Organization
        fields = '__all__'

    def get_accounts_group_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountsGroupObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountsGroupObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_account_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

class OrganizationEditSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), required=False)

    class Meta:
        model = Organization
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class SubdivisionSerializer(serializers.ModelSerializer):
    group = AccountsGroupBaseSerializer()
    organization = OrganizationBaseSerializer()
    parent_subdivision = SubdivisionBaseSerializer()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Subdivision
        fields = '__all__'

    def get_accounts_group_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountsGroupObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountsGroupObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_account_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

class SubdivisionEditSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), required=False)
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=False)
    parent_subdivision = serializers.PrimaryKeyRelatedField(queryset=Subdivision.objects.all(), required=False)

    class Meta:
        model = Subdivision
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class PositionSerializer(serializers.ModelSerializer):
    group = AccountsGroupBaseSerializer()
    subdivision = SubdivisionBaseSerializer()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Position
        fields = '__all__'

    def get_accounts_group_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountsGroupObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountsGroupObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_account_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

class PositionEditSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), required=False)
    subdivision = serializers.PrimaryKeyRelatedField(queryset=Subdivision.objects.all(), required=False)

    class Meta:
        model = Position
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)


class PlacementSerializer(serializers.ModelSerializer):
    account = AccountBaseSerializer()
    position = PositionBaseSerializer()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Placement
        fields = '__all__'

class PlacementEditSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())

    class Meta:
        model = Placement
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('username', 'email', 'password', 'legal_agree', 'policy_agree')

    def create(self, validated_data):
        user = Account.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class HomePageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    str = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = HomePage
        fields = '__all__'

    def get_str(self, obj):
        return f"{obj.title}"

    def get_accounts_group_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountsGroupObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountsGroupObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_account_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

class HomePageEditSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False, style={'base_template': 'textarea.html'})

    class Meta:
        model = HomePage
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class LegalPageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    str = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = LegalPage
        fields = '__all__'

    def get_str(self, obj):
        return f"{obj.title}"

    def get_accounts_group_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountsGroupObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountsGroupObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_account_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

class LegalPageEditSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False, style={'base_template': 'textarea.html'})

    class Meta:
        model = LegalPage
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class PolicyPageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    str = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = PolicyPage
        fields = '__all__'

    def get_str(self, obj):
        return f"{obj.title}"

    def get_accounts_group_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountsGroupObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountsGroupObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

    def get_account_object_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        permissions = AccountObjectPermission.objects.filter(
            content_type=content_type,
            object_pk=obj.pk
        )
        return AccountObjectPermissionBaseSerializer(permissions, many=True, context=self.context).data

class PolicyPageEditSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False, style={'base_template': 'textarea.html'})

    class Meta:
        model = PolicyPage
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)
