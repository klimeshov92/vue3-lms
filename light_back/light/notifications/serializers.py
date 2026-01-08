
from rest_framework import serializers
from .models import *
from core.models import Account, AccountObjectPermission, AccountsGroupObjectPermission
from bpms.models import *
from bpms.serializers import *
from django.conf import settings
from django.http import HttpResponse
import os
from core.serializers import AccountBaseSerializer, AccountObjectPermissionBaseSerializer, AccountsGroupObjectPermissionBaseSerializer

import logging
logger = logging.getLogger('project')

class NotificationSettingsBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()

    class Meta:
        model = NotificationSettings
        fields = '__all__'

    def get_str(self, obj):
        return f"{obj.account}"

class NotificationSettingsSerializer(serializers.ModelSerializer):
    account = AccountBaseSerializer(required=False)
    str = serializers.SerializerMethodField()

    class Meta:
        model = NotificationSettings
        fields = '__all__'

    def get_str(self, obj):
        return f"{obj.account.username}"

class NotificationSettingsEditSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)

    class Meta:
        model = NotificationSettings
        fields = '__all__'

class TaskNotificationBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = TaskNotification
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.task} - {obj.get_notification_type_display()} - {obj.created.strftime("%d.%m.%Y %H:%M")}'

class TaskNotificationSerializer(serializers.ModelSerializer):
    task = TaskBaseSerializer(required=False)
    account = AccountBaseSerializer(required=False)
    str = serializers.SerializerMethodField()
    notification_type_display = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = TaskNotification
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.task} - {obj.get_notification_type_display()} - {obj.created.strftime("%d.%m.%Y %H:%M")}'

    def get_notification_type_display(self, obj):
        return obj.get_notification_type_display()

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

