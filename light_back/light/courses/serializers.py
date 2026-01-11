
from rest_framework import serializers
from .models import *
from core.models import *
from core.serializers import *
from bpms.models import *
from bpms.serializers import *
from django.conf import settings
from django.http import HttpResponse
import os

import logging
logger = logging.getLogger('project')

class CourseBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_str(self, obj):
        return f"{obj.name}"

class LastTaskBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.get_task_type_display()} - {obj.name}'


class CourseSerializer(serializers.ModelSerializer):
    constructor_type_display = serializers.SerializerMethodField()
    categories = CategoryBaseSerializer(many=True, required=False)
    avatar = serializers.ImageField(required=False)
    upload_file = serializers.FileField(required=False)
    str = serializers.SerializerMethodField()
    last_task = serializers.SerializerMethodField()
    self_assignment_task_template = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_constructor_type_display(self, obj):
        return obj.get_constructor_type_display()

    def get_str(self, obj):
        return f"{obj.name}"

    def get_last_task(self, obj):
        last_task = Task.objects.filter(
            course_id=obj.id,
            executor=self.context['request'].user,
            course_result__isnull=False,
        ).exclude(course_result__status__in=['canceled', 'failed']).order_by('-id').first()
        return LastTaskBaseSerializer(last_task, context=self.context).data if last_task else None

    def get_self_assignment_task_template(self, obj):
        self_assignment_task_template = TaskTemplate.objects.filter(
            course_id=obj.id,
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

class CourseEditSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    upload_file = serializers.FileField(required=False)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

