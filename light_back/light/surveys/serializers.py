
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

class SurveyBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Survey
        fields = '__all__'

    def get_str(self, obj):
        return f"{obj.name}"

class SurveyResultSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = SurveyResult
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_str(self, obj):
        return f'{obj.task} - {obj.get_status_display()}'

class LastTaskBaseSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_result(self, obj):
        if obj.task_type == 'survey_taking':
            result = obj.survey_result
            return SurveyResultSerializer(result, context=self.context).data

    def get_str(self, obj):
        return f'{obj.get_task_type_display()} - {obj.name}'

from comments.models import *
class TopicBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Topic
        fields = '__all__'

    def get_str(self, obj):
        return f"{obj.get_topic_type_display()} - {obj.name}"


class SurveySerializer(serializers.ModelSerializer):
    categories = CategoryBaseSerializer(many=True, required=False)
    avatar = serializers.ImageField(required=False)
    survey_sections = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    last_task = serializers.SerializerMethodField()
    self_assignment_task_template = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Survey
        fields = '__all__'

    def get_survey_sections(self, obj):
        survey_sections = SurveySection.objects.filter(survey=obj).order_by('item')
        return SurveySectionSerializer(survey_sections, many=True, context=self.context).data

    def get_str(self, obj):
        return f"{obj.name}"

    def get_topic(self, obj):
        topic = Topic.objects.filter(
            survey_id=obj.id,
        ).order_by('-id').first()
        return TopicBaseSerializer(topic, context=self.context).data if topic else None

    def get_last_task(self, obj):
        last_task = Task.objects.filter(
            survey_id=obj.id,
            executor=self.context['request'].user,
        ).order_by('-id').first()
        return LastTaskBaseSerializer(last_task, context=self.context).data if last_task else None

    def get_self_assignment_task_template(self, obj):
        self_assignment_task_template = TaskTemplate.objects.filter(
            survey_id=obj.id,
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

class SurveyEditSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)

    class Meta:
        model = Survey
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class SurveySectionBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = SurveySection
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.survey.name} | {obj.item} - {obj.name}'

class SurveySectionSerializer(serializers.ModelSerializer):
    survey = SurveyBaseSerializer(required=False)
    survey_section_survey_questions = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = SurveySection
        fields = '__all__'

    def get_survey_section_survey_questions(self, obj):
        survey_section_survey_questions = SurveySectionQuestion.objects.filter(survey_section=obj).order_by('item')
        return SurveySectionQuestionSerializer(survey_section_survey_questions, many=True, context=self.context).data

    def get_str(self, obj):
        return f'{obj.survey.name} | {obj.item} - {obj.name}'

class SurveySectionEditSerializer(serializers.ModelSerializer):
    survey = serializers.PrimaryKeyRelatedField(queryset=Survey.objects.all(), required=False)
    class Meta:
        model = SurveySection
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class SurveyQuestionBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Question
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.get_survey_question_type_display()} - {obj.text}'

class SurveyQuestionSerializer(serializers.ModelSerializer):
    survey_question_type_display = serializers.SerializerMethodField()
    survey_answers = serializers.SerializerMethodField()
    picture = serializers.ImageField(required=False)
    categories = CategoryBaseSerializer(many=True, required=False)
    str = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = SurveyQuestion
        fields = '__all__'

    def get_survey_question_type_display(self, obj):
        return obj.get_survey_question_type_display()

    def get_survey_answers(self, obj):
        survey_answers = Answer.objects.filter(survey_question=obj).order_by('item')
        return AnswerSerializer(survey_answers, many=True, context=self.context).data

    def get_str(self, obj):
        return f'{obj.get_survey_question_type_display()} - {obj.text}'

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

class SurveyQuestionEditSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(required=False)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)
    class Meta:
        model = SurveyQuestion
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class SurveySectionQuestionSerializer(serializers.ModelSerializer):
    survey_section = SurveySectionBaseSerializer(required=False)
    survey_question = SurveyQuestionSerializer(required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = SurveySectionQuestion
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.survey_section.name} - {obj.item} | {obj.survey_question}'

class SurveySectionQuestionEditSerializer(serializers.ModelSerializer):
    survey_section = serializers.PrimaryKeyRelatedField(queryset=SurveySection.objects.all(), required=False)
    survey_question = serializers.PrimaryKeyRelatedField(queryset=SurveyQuestion.objects.all(), required=False)
    class Meta:
        model = SurveySectionQuestion
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class SurveyAnswerBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = SurveyAnswer
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.survey_question.get_survey_question_type_display()} - {obj.survey_question.text} | {obj.item} - {obj.text}'

class SurveyAnswerSerializer(serializers.ModelSerializer):
    survey_question = SurveyQuestionBaseSerializer(required=False)
    picture = serializers.ImageField(required=False)
    relevant_point = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = SurveyAnswer
        fields = '__all__'

    def get_relevant_point(self, obj):
        relevant_point = RelevantPoint.objects.filter(survey_answer=obj).first()
        return RelevantPointSerializer(relevant_point).data

    def get_str(self, obj):
        return f'{obj.survey_question.get_survey_question_type_display()} - {obj.survey_question.text} | {obj.item} - {obj.text}'

class SurveyAnswerEditSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(required=False)
    survey_question = serializers.PrimaryKeyRelatedField(queryset=SurveyQuestion.objects.all(), required=False)
    class Meta:
        model = SurveyAnswer
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)
