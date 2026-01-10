
from rest_framework import serializers
from .models import *
from core.models import *
from bpms.models import *
from core.serializers import *
from materials.serializers import *
from files.serializers import *
from bpms.serializers import *
from django.conf import settings
from django.http import HttpResponse
import os

import logging
logger = logging.getLogger('project')

class EventTemplateBaseSerializer(serializers.ModelSerializer):
    admins = AccountBaseSerializer(many=True, required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = EventTemplate
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.name}'

class EventTemplateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    format_display = serializers.SerializerMethodField()
    categories = CategoryBaseSerializer(many=True, required=False)
    admins = AccountBaseSerializer(many=True, required=False)
    str = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = EventTemplate
        fields = '__all__'

    def get_format_display(self, obj):
        return obj.get_format_display()

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

class EventTemplateEditSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)
    admins = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), many=True, required=False)

    class Meta:
        model = EventTemplate
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user

        instance = super().create(validated_data)
        instance.admin_group = AccountsGroup.objects.create(
            name=f"Админы мероприятия [{instance.id}]",
            type='admin_group'
        )
        instance.admin_group.user_set.set(instance.admins.all())
        instance.save()

        return instance

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user

        instance = super().update(instance, validated_data)
        instance.admin_group.user_set.set(instance.admins.all())
        instance.save()

        return instance

class EventSlotBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = EventSlot
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.event_template.name} - {obj.planned_start.strftime("%d.%m.%Y %H:%M")}'

class LastTaskBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.get_task_type_display()} - {obj.name}'

class EventSlotSerializer(serializers.ModelSerializer):
    event_template = EventTemplateSerializer(required=False)
    status_display = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    last_task = serializers.SerializerMethodField()
    self_assignment_task_template = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = EventSlot
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_str(self, obj):
        return f'{obj.event_template.name} - {obj.planned_start.strftime("%d.%m.%Y %H:%M")}'

    def get_last_task(self, obj):
        last_task = Task.objects.filter(
            event_slot_id=obj.id,
            executor=self.context['request'].user,
        ).order_by('-id').first()
        return LastTaskBaseSerializer(last_task, context=self.context).data

    def get_self_assignment_task_template(self, obj):
        self_assignment_task_template = TaskTemplate.objects.filter(
            event_slot_id=obj.id,
            self_assignment=True,
        ).first()
        self_assignment_task_template_id = self_assignment_task_template.id if self_assignment_task_template else None
        return self_assignment_task_template_id

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

class EventSlotEditSerializer(serializers.ModelSerializer):
    event_template = serializers.PrimaryKeyRelatedField(queryset=EventTemplate.objects.all(), required=False, allow_null=True)

    class Meta:
        model = EventSlot
        fields = '__all__'


    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)


