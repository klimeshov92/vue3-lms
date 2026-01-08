
from rest_framework import serializers
from .models import *
from core.models import *
from core.serializers import *
from bpms.models import *
from bpms.serializers import *
from django.conf import settings

import logging
logger = logging.getLogger('project')

class TopicBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Topic
        fields = '__all__'

    def get_str(self, obj):
        return f"{obj.get_topic_type_display()} - {obj.name}"


class TopicSerializer(serializers.ModelSerializer):
    topic_type_display = serializers.SerializerMethodField()
    task = TaskBaseSerializer(required=False)
    queue = QueueBaseSerializer(required=False)
    str = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Topic
        fields = '__all__'

    def get_topic_type_display(self, obj):
        return obj.get_topic_type_display()

    def get_str(self, obj):
        return f"{obj.get_topic_type_display()} - {obj.name}"

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

class TopicEditSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)
    queue = serializers.PrimaryKeyRelatedField(queryset=Queue.objects.all(), required=False)

    class Meta:
        model = Topic
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class ParentCommentSerializer(serializers.ModelSerializer):
    sender = AccountBaseSerializer(required=False)

    class Meta:
        model = Comment
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    topic = TopicBaseSerializer(required=False)
    parent_comment = ParentCommentSerializer(required=False)
    sender = AccountBaseSerializer(required=False)
    recipient = AccountBaseSerializer(required=False, allow_null=True)
    content = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    str = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_str(self, obj):
        return f"{obj.topic.name} - {obj.id}"

class CommentEditSerializer(serializers.ModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all(), required=False)
    parent_comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)
    sender = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)
    recipient = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)
    content = serializers.CharField(required=False, style={'base_template': 'textarea.html'})

    class Meta:
        model = Comment
        fields = '__all__'