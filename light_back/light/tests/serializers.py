
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

class TestBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Test
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

class TestSerializer(serializers.ModelSerializer):
    categories = CategoryBaseSerializer(many=True, required=False)
    avatar = serializers.ImageField(required=False)
    test_sections = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    last_task = serializers.SerializerMethodField()
    self_assignment_task_template = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Test
        fields = '__all__'

    def get_test_sections(self, obj):
        test_sections = TestSection.objects.filter(test=obj).order_by('item')
        return TestSectionSerializer(test_sections, many=True, context=self.context).data

    def get_str(self, obj):
        return f"{obj.name}"

    def get_last_task(self, obj):
        last_task = Task.objects.filter(
            test_id=obj.id,
            executor=self.context['request'].user,
        ).order_by('-id').first()
        return LastTaskBaseSerializer(last_task, context=self.context).data if last_task else None

    def get_self_assignment_task_template(self, obj):
        self_assignment_task_template = TaskTemplate.objects.filter(
            test_id=obj.id,
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

class TestEditSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)

    class Meta:
        model = Test
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class TestSectionBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = TestSection
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.test.name} | {obj.item} - {obj.name}'

class TestSectionSerializer(serializers.ModelSerializer):
    test = TestBaseSerializer(required=False)
    test_section_questions = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = TestSection
        fields = '__all__'

    def get_test_section_questions(self, obj):
        test_section_questions = TestSectionQuestion.objects.filter(test_section=obj).order_by('item')
        return TestSectionQuestionSerializer(test_section_questions, many=True, context=self.context).data

    def get_str(self, obj):
        return f'{obj.test.name} | {obj.item} - {obj.name}'

class TestSectionEditSerializer(serializers.ModelSerializer):
    test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all(), required=False)
    class Meta:
        model = TestSection
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class QuestionBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Question
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.get_question_type_display()} - {obj.text}'

class QuestionSerializer(serializers.ModelSerializer):
    question_type_display = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    picture = serializers.ImageField(required=False)
    categories = CategoryBaseSerializer(many=True, required=False)
    str = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Question
        fields = '__all__'

    def get_question_type_display(self, obj):
        return obj.get_question_type_display()

    def get_answers(self, obj):
        answers = Answer.objects.filter(question=obj).order_by('item')
        return AnswerSerializer(answers, many=True, context=self.context).data

    def get_str(self, obj):
        return f'{obj.get_question_type_display()} - {obj.text}'

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

class QuestionEditSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(required=False)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)
    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class TestSectionQuestionSerializer(serializers.ModelSerializer):
    test_section = TestSectionBaseSerializer(required=False)
    question = QuestionSerializer(required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = TestSectionQuestion
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.test_section.name} - {obj.item} | {obj.question}'

class TestSectionQuestionEditSerializer(serializers.ModelSerializer):
    test_section = serializers.PrimaryKeyRelatedField(queryset=TestSection.objects.all(), required=False)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)
    class Meta:
        model = TestSectionQuestion
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class AnswerBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Answer
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.question.get_question_type_display()} - {obj.question.text} | {obj.item} - {obj.text}'

class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionBaseSerializer(required=False)
    picture = serializers.ImageField(required=False)
    relevant_point = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Answer
        fields = '__all__'

    def get_relevant_point(self, obj):
        relevant_point = RelevantPoint.objects.filter(answer=obj).first()
        return RelevantPointSerializer(relevant_point).data

    def get_str(self, obj):
        return f'{obj.question.get_question_type_display()} - {obj.question.text} | {obj.item} - {obj.text}'

class AnswerEditSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(required=False)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)
    class Meta:
        model = Answer
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class RelevantPointSerializer(serializers.ModelSerializer):
    answer = AnswerBaseSerializer(required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = RelevantPoint
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.answer} | {obj.text}'

class RelevantPointEditSerializer(serializers.ModelSerializer):
    answer = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all(), required=False)
    class Meta:
        model = RelevantPoint
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)
