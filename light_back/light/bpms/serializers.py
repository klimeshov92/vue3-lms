
from rest_framework import serializers
from .models import *
from core.models import *
from core.serializers import *
from news.serializers import *
from news.models import *
from materials.serializers import *
from materials.models import *
from courses.serializers import *
from courses.models import *
from tests.serializers import *
from tests.models import *
from events.serializers import *
from events.models import *
from django.conf import settings
import json

import logging
logger = logging.getLogger('project')

class InteractionSerializer(serializers.ModelSerializer):
    categories = CategoryBaseSerializer(many=True, required=False)
    object_type_display = serializers.SerializerMethodField()
    client = ClientBaseSerializer(required=False)
    account = AccountBaseSerializer(required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Interaction
        fields = '__all__'

    def get_object_type_display(self, obj):
        return obj.get_object_type_display()

    def get_str(self, obj):
        if obj.object_type == 'client':
            object_name = obj.client if obj.client else 'Объект не найден'
        elif obj.object_type == 'account':
            object_name = obj.account if obj.account else 'Объект не найден'
        return f'{obj.id} - {obj.get_object_type_display()} - {object_name}'

class InteractionEditSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False, allow_null=True)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), required=False, allow_null=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)

    class Meta:
        model = Interaction
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class TaskTemplateBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = TaskTemplate
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.get_task_type_display()} - {obj.name}'

class TaskTemplateSerializer(serializers.ModelSerializer):
    #object_type_display = serializers.SerializerMethodField()
    plan = TaskTemplateBaseSerializer(required=False)
    categories = CategoryBaseSerializer(many=True, required=False)
    task_type_display = serializers.SerializerMethodField()
    new = NewBaseSerializer(required=False)
    material = MaterialBaseSerializer(required=False)
    course = CourseBaseSerializer(required=False)
    test = TestBaseSerializer(required=False)
    event_template = EventTemplateBaseSerializer(required=False)
    event_slot = EventSlotBaseSerializer(required=False)
    manual = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    term_type_display = serializers.SerializerMethodField()
    delay_type_display = serializers.SerializerMethodField()
    child_task_templates = serializers.SerializerMethodField()
    control_elements = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = TaskTemplate
        fields = '__all__'

    #def get_object_type_display(self, obj):
        #return obj.get_object_type_display()

    def get_task_type_display(self, obj):
        return obj.get_task_type_display()

    def get_term_type_display(self, obj):
        return obj.get_term_type_display()

    def get_delay_type_display(self, obj):
        return obj.get_delay_type_display()

    def get_child_task_templates(self, obj):
        child_task_templates = TaskTemplate.objects.filter(plan=obj).order_by('item')
        return TaskTemplateSerializer(child_task_templates, many=True, context=self.context).data

    def get_control_elements(self, obj):
        control_elements = ControlElement.objects.filter(task_template=obj)
        return ControlElementBaseSerializer(control_elements, many=True, context=self.context).data

    def get_str(self, obj):
        if obj.item:
            return f'{obj.get_task_type_display()} - {obj.item} - {obj.name}'
        else:
            return f'{obj.get_task_type_display()} - {obj.name}'

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

class TaskTemplateEditSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=TaskTemplate.objects.all(), required=False, allow_null=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)
    new = serializers.PrimaryKeyRelatedField(queryset=New.objects.all(), required=False)
    material = serializers.PrimaryKeyRelatedField(queryset=Material.objects.all(), required=False)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False)
    test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all(), required=False)
    event_template = serializers.PrimaryKeyRelatedField(queryset=EventTemplate.objects.all(), required=False)
    event_slot = serializers.PrimaryKeyRelatedField(queryset=EventSlot.objects.all(), required=False)
    manual = serializers.CharField(required=False, style={'base_template': 'textarea.html'})

    class Meta:
        model = TaskTemplate
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class PublicTaskSerializer(serializers.ModelSerializer):
    task_template = TaskTemplateBaseSerializer(required=False)
    categories = CategoryBaseSerializer(many=True, required=False)
    str = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = PublicTask
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

class PublicTaskEditSerializer(serializers.ModelSerializer):
    task_template = serializers.PrimaryKeyRelatedField(queryset=TaskTemplate.objects.all(), required=False, allow_null=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)

    class Meta:
        model = PublicTask
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class PublicPlanSerializer(serializers.ModelSerializer):
    task_template = TaskTemplateBaseSerializer(required=False)
    categories = CategoryBaseSerializer(many=True, required=False)
    str = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = PublicPlan
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

class PublicPlanEditSerializer(serializers.ModelSerializer):
    task_template = serializers.PrimaryKeyRelatedField(queryset=TaskTemplate.objects.all(), required=False, allow_null=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)

    class Meta:
        model = PublicPlan
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class TaskBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.get_task_type_display()} - {obj.name}'

class ResultTaskSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    outcomes = serializers.SerializerMethodField()
    material = MaterialСontentSerializer()
    new = NewСontentSerializer()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.get_task_type_display()} - {obj.name}'

    def get_outcomes(self, obj):
        outcomes = ControlElement.objects.filter(task_template=obj.task_template)
        return ControlElementSerializer(outcomes, many=True, context=self.context).data

class TaskSerializer(serializers.ModelSerializer):
    #object_type_display = serializers.SerializerMethodField()
    task_template = TaskTemplateBaseSerializer(required=False)
    interaction = InteractionSerializer(required=False)
    plan = TaskBaseSerializer(required=False)
    task_type_display = serializers.SerializerMethodField()
    new = NewBaseSerializer(required=False)
    material = MaterialBaseSerializer(required=False)
    course = CourseBaseSerializer(required=False)
    test = TestBaseSerializer(required=False)
    event_template = EventTemplateBaseSerializer(required=False)
    event_slot = EventSlotBaseSerializer(required=False)
    manual = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    executor = AccountBaseSerializer(required=False)
    co_executors = AccountBaseSerializer(many=True, required=False)
    controllers = AccountBaseSerializer(many=True, required=False)
    observers = AccountBaseSerializer(many=True, required=False)
    co_executor_group = AccountsGroupBaseSerializer(required=False)
    controller_group = AccountsGroupBaseSerializer(required=False)
    observer_group = AccountsGroupBaseSerializer(required=False)
    categories = CategoryBaseSerializer(many=True, required=False)
    child_tasks = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()
    outcomes = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = '__all__'

    #def get_object_type_display(self, obj):
        #return obj.get_object_type_display()

    def get_task_type_display(self, obj):
        return obj.get_task_type_display()

    def get_child_tasks(self, obj):
        child_tasks = Task.objects.filter(plan=obj).order_by('item')
        return TaskSerializer(child_tasks, many=True, context=self.context).data

    def get_result(self, obj):
        if obj.task_type == 'common_task':
            result = obj.task_result
            return TaskResultSerializer(result, context=self.context).data
        elif obj.task_type == 'plan_implementation':
            result = obj.plan_result
            return PlanResultSerializer(result, context=self.context).data
        elif obj.task_type == 'news_reading':
            result = obj.new_result
            return MaterialResultSerializer(result, context=self.context).data
        elif obj.task_type == 'material_review':
            result = obj.material_result
            return MaterialResultSerializer(result, context=self.context).data
        elif obj.task_type == 'course_study':
            result = obj.course_result
            return CourseResultSerializer(result, context=self.context).data
        elif obj.task_type == 'test_taking':
            result = obj.test_result
            return TestResultSerializer(result, context=self.context).data
        elif obj.task_type == 'event_participation':
            result = obj.event_result
            return EventResultSerializer(result, context=self.context).data

    def get_outcomes(self, obj):
        outcomes = ControlElement.objects.filter(task_template=obj.task_template)
        return ControlElementSerializer(outcomes, many=True, context=self.context).data

    def get_str(self, obj):
        if obj.item:
            return f'{obj.get_task_type_display()} - {obj.item} - {obj.name}'
        else:
            return f'{obj.get_task_type_display()} - {obj.name}'

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

class TaskEditSerializer(serializers.ModelSerializer):
    interaction = serializers.PrimaryKeyRelatedField(queryset=Interaction.objects.all(), required=False)
    plan = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)
    new = serializers.PrimaryKeyRelatedField(queryset=New.objects.all(), required=False)
    material = serializers.PrimaryKeyRelatedField(queryset=Material.objects.all(), required=False)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False)
    test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all(), required=False)
    event_template = serializers.PrimaryKeyRelatedField(queryset=EventTemplate.objects.all(), required=False)
    event_slot = serializers.PrimaryKeyRelatedField(queryset=EventSlot.objects.all(), required=False)
    executor = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)
    co_executors = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), many=True, required=False)
    controllers = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), many=True, required=False)
    observers = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), many=True, required=False)
    manual = serializers.CharField(required=False, style={'base_template': 'textarea.html'})
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user

        # Создаем задачу.
        instance = super().create(validated_data)

        # Создаем и назначаем группы.
        instance.co_executor_group = AccountsGroup.objects.create(
            name=f"Соисполнители задачи [{instance.id}]",
            type='task_co_executors'
        )
        instance.controller_group = AccountsGroup.objects.create(
            name=f"Контролеры задачи [{instance.id}]",
            type='task_co_controllers'
        )
        instance.observer_group = AccountsGroup.objects.create(
            name=f"Наблюдатели задачи [{instance.id}]",
            type='task_co_observers'
        )

        # Добавляем пользователей в группы.
        instance.co_executor_group.user_set.set(instance.co_executors.all())
        instance.controller_group.user_set.set(instance.controllers.all())
        instance.observer_group.user_set.set(instance.observers.all())

        # Сохраняем обновленную задачу.
        instance.save()

        return instance

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user

        # Обновляем задачу.
        instance = super().update(instance, validated_data)

        # Обновляем группы.
        instance.co_executor_group.user_set.set(instance.co_executors.all())
        instance.controller_group.user_set.set(instance.controllers.all())
        instance.observer_group.user_set.set(instance.observers.all())

        # Сохраняем изменения в задаче.
        instance.save()

        return instance

class TaskTemplateAssignmentSerializer(serializers.ModelSerializer):
    task_template = TaskTemplateBaseSerializer(required=False)
    interaction = InteractionSerializer(required=False)
    executor_type_display = serializers.SerializerMethodField()
    executor = AccountBaseSerializer(required=False)
    executor_group = AccountsGroupBaseSerializer(required=False)
    controller_group = AccountsGroupBaseSerializer(required=False)
    observer_group = AccountsGroupBaseSerializer(required=False)
    categories = CategoryBaseSerializer(many=True, required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = TaskTemplateAssignment
        fields = '__all__'

    def get_executor_type_display(self, obj):
        return obj.get_executor_type_display()

    def get_str(self, obj):
        return f'{obj.task_template} - {obj.executor_group if obj.executor_group else obj.executor}'

class TaskTemplateAssignmentEditSerializer(serializers.ModelSerializer):
    task_template = serializers.PrimaryKeyRelatedField(queryset=TaskTemplate.objects.all(), required=False)
    interaction = serializers.PrimaryKeyRelatedField(queryset=Interaction.objects.all(), required=False)
    executor = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)
    executor_group = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), required=False)
    controller_group = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), required=False)
    observer_group = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), required=False)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)

    class Meta:
        model = TaskTemplateAssignment
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class QueueBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Queue
        fields = '__all__'

    def get_str(self, obj):
        return obj.name

class QueueSerializer(serializers.ModelSerializer):
    categories = CategoryBaseSerializer(many=True, required=False)
    queue_executors = serializers.SerializerMethodField()
    queue_tasks = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = Queue
        fields = '__all__'

    def get_queue_executors(self, obj):
        queue_executors = QueueExecutor.objects.filter(queue=obj)
        return QueueExecutorSerializer(queue_executors, many=True, context=self.context).data

    def get_queue_tasks(self, obj):
        queue_tasks = QueueTask.objects.filter(queue=obj)
        return QueueTaskSerializer(queue_tasks, many=True, context=self.context).data

    def get_str(self, obj):
        return obj.name

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

class QueueEditSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)

    class Meta:
        model = Queue
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class QueueExecutorSerializer(serializers.ModelSerializer):
    queue = QueueBaseSerializer(required=False)
    executor = AccountBaseSerializer(required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = QueueExecutor
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.queue} - {obj.executor}'

class QueueExecutorEditSerializer(serializers.ModelSerializer):
    queue = serializers.PrimaryKeyRelatedField(queryset=Queue.objects.all(), required=False)
    executor = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)

    class Meta:
        model = QueueExecutor
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class QueueTaskSerializer(serializers.ModelSerializer):
    queue = QueueBaseSerializer(required=False)
    task = TaskBaseSerializer(required=False)
    executor = AccountBaseSerializer(required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = QueueTask
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.queue} - {obj.task}'

class QueueTaskEditSerializer(serializers.ModelSerializer):
    queue = serializers.PrimaryKeyRelatedField(queryset=Queue.objects.all(), required=False)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)
    executor = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)

    class Meta:
        model = QueueTask
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class ControlElementBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = ControlElement
        fields = '__all__'

    def get_str(self, obj):
        return obj.name

class ControlElementSerializer(serializers.ModelSerializer):
    type_of_work_display = serializers.SerializerMethodField()
    #object_type_display = serializers.SerializerMethodField()
    task_template = TaskTemplateBaseSerializer(required=False)
    categories = CategoryBaseSerializer(many=True, required=False)
    control_element_events = serializers.SerializerMethodField()
    control_element_conditions = serializers.SerializerMethodField()
    control_element_actions = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    accounts_group_object_permissions = serializers.SerializerMethodField()
    account_object_permissions = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = ControlElement
        fields = '__all__'

    def get_type_of_work_display(self, obj):
        return obj.get_type_of_work_display()

    #def get_object_type_display(self, obj):
        #return obj.get_object_type_display()

    def get_control_element_events(self, obj):
        event = ControlElementEvent.objects.filter(control_element=obj)
        return ControlElementEventSerializer(event, many=True, context=self.context).data

    def get_control_element_conditions(self, obj):
        condition = ControlElementCondition.objects.filter(control_element=obj).order_by('item')
        return ControlElementConditionSerializer(condition, many=True, context=self.context).data

    def get_control_element_actions(self, obj):
        actions = ControlElementAction.objects.filter(control_element=obj).order_by('item')
        return ControlElementActionSerializer(actions, many=True, context=self.context).data

    def get_str(self, obj):
        return obj.name

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

class ControlElementEditSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)
    task_template = serializers.PrimaryKeyRelatedField(queryset=TaskTemplate.objects.all(), required=False)

    class Meta:
        model = ControlElement
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class ControlElementEventSerializer(serializers.ModelSerializer):
    control_element = ControlElementBaseSerializer(required=False)
    event_type_display = serializers.SerializerMethodField()
    period_display = serializers.SerializerMethodField()
    task_template = TaskTemplateSerializer(required=False)
    fired_trigger = ControlElementBaseSerializer(required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = ControlElementEvent
        fields = '__all__'

    def get_event_type_display(self, obj):
        return obj.get_event_type_display()

    def get_period_display(self, obj):
        return obj.get_period_display()

    def get_str(self, obj):
        if obj.event_type == 'task_created':
            return f'{obj.control_element} - {obj.get_event_type_display()} - {obj.task_template}'
        elif obj.event_type == 'task_status_changed':
            return f'{obj.control_element} - {obj.get_event_type_display()} - {obj.task_template}'
        elif obj.event_type == 'task_outcome_changed':
            return f'{obj.control_element} - {obj.get_event_type_display()} - {obj.task_template}'
        elif obj.event_type == 'trigger_fired':
            return f'{obj.control_element} - {obj.get_event_type_display()} - {obj.fired_trigger}'
        elif obj.event_type == 'periodic_event':
            return f'{obj.control_element} - {obj.get_event_type_display()} - {obj.task_template} - {obj.get_period_display()} - {obj.start_time.strftime("%d.%m.%Y %H:%M")}'
        return f'{obj.control_element} - {obj.event_type}'

class ControlElementEventEditSerializer(serializers.ModelSerializer):
    control_element = serializers.PrimaryKeyRelatedField(queryset=ControlElement.objects.all(), required=False)
    task_template = serializers.PrimaryKeyRelatedField(queryset=TaskTemplate.objects.all(), allow_null=True, required=False)
    fired_trigger = serializers.PrimaryKeyRelatedField(queryset=ControlElement.objects.all(), allow_null=True, required=False)

    class Meta:
        model = ControlElementEvent
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class ControlElementConditionSerializer(serializers.ModelSerializer):
    control_element = ControlElementBaseSerializer(required=False)
    logic_operator_display = serializers.SerializerMethodField()
    condition_type_display = serializers.SerializerMethodField()
    task_template = TaskTemplateSerializer(required=False)
    comparison_operator_display = serializers.SerializerMethodField()
    order_operator_display = serializers.SerializerMethodField()
    task_status_display = serializers.SerializerMethodField()
    task_outcome = ControlElementBaseSerializer(required=False)
    target_task_display = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = ControlElementCondition
        fields = '__all__'

    def get_logic_operator_display(self, obj):
        return obj.get_logic_operator_display()

    def get_condition_type_display(self, obj):
        return obj.get_condition_type_display()

    def get_comparison_operator_display(self, obj):
        return obj.get_comparison_operator_display()

    def get_order_operator_display(self, obj):
        return obj.get_order_operator_display()

    def get_task_status_display(self, obj):
        return obj.get_task_status_display()

    def get_target_task_display(self, obj):
        return obj.get_target_task_display()

    def get_str(self, obj):
        if obj.condition_type == 'task_not_exists':
            return f'{obj.control_element} - {obj.get_condition_type_display()} - {obj.task_template.name}'
        elif obj.condition_type == 'child_tasks_status':
            return f'{obj.control_element} - {obj.get_condition_type_display()} - {obj.task_template.name} - {obj.get_comparison_operator_display()} - {obj.get_task_status_display()}'
        elif obj.condition_type == 'task_status':
            return f'{obj.control_element} - {obj.get_condition_type_display()} - {obj.task_template.name} - {obj.get_comparison_operator_display()} - {obj.get_task_status_display()}'
        elif obj.condition_type == 'task_outcome':
            return f'{obj.control_element} - {obj.get_condition_type_display()} - {obj.task_template.name} - {obj.get_comparison_operator_display()} - {obj.task_outcome}'
        elif obj.condition_type == 'days_worked':
            return f'{obj.control_element} - {obj.get_condition_type_display()} - {obj.get_order_operator_display()} - {obj.days_worked}'
        return f'Неизвестный тип условия'


class ControlElementConditionEditSerializer(serializers.ModelSerializer):
    control_element = serializers.PrimaryKeyRelatedField(queryset=ControlElement.objects.all(), required=False)
    task_template = serializers.PrimaryKeyRelatedField(queryset=TaskTemplate.objects.all(), allow_null=True, required=False)
    task_outcome = serializers.PrimaryKeyRelatedField(queryset=ControlElement.objects.all(), allow_null=True, required=False)

    class Meta:
        model = ControlElementCondition
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class ControlElementActionSerializer(serializers.ModelSerializer):
    control_element = ControlElementBaseSerializer(required=False)
    action_type_display = serializers.SerializerMethodField()
    task_template = TaskTemplateSerializer(required=False)
    queue = QueueSerializer(required=False)
    task_status_display = serializers.SerializerMethodField()
    task_outcome = ControlElementBaseSerializer(required=False)
    target_task_display = serializers.SerializerMethodField()
    target_group = AccountsGroupBaseSerializer(required=False)
    target_interaction_display = serializers.SerializerMethodField()
    executor_type_display = serializers.SerializerMethodField()
    executor = AccountBaseSerializer(required=False)
    controller_group = AccountsGroupBaseSerializer(required=False)
    observer_group = AccountsGroupBaseSerializer(required=False)
    delay_type_display = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = ControlElementAction
        fields = '__all__'

    def get_action_type_display(self, obj):
        return obj.get_action_type_display()

    def get_task_status_display(self, obj):
        return obj.get_task_status_display()

    def get_target_task_display(self, obj):
        return obj.get_target_task_display()

    def get_target_interaction_display(self, obj):
        return obj.get_target_interaction_display()

    def get_executor_type_display(self, obj):
        return obj.get_executor_type_display()

    def get_delay_type_display(self, obj):
        return obj.get_delay_type_display()

    def get_str(self, obj):
        if obj.action_type == 'change_task_status':
            return f'{obj.control_element} - {obj.get_action_type_display()} -  {obj.task_template} - {obj.get_task_status_display()}'
        elif obj.action_type == 'change_task_outcome':
            return f'{obj.control_element} - {obj.get_action_type_display()} -  {obj.task_template} - {obj.task_outcome}'
        elif obj.action_type == 'assign_task':
            return f'{obj.control_element} - {obj.get_action_type_display()} -  {obj.task_template} - {obj.get_executor_type_display()}'
        elif obj.action_type == 'add_task_to_queue':
            return f'{obj.control_element} - {obj.get_action_type_display()} -  {obj.task_template} - {obj.queue}'
        elif obj.action_type == 'add_to_group':
            return f'{obj.control_element} - {obj.get_action_type_display()} -  {obj.target_group}'
        elif obj.action_type == 'remove_from_group':
            return f'{obj.control_element} - {obj.get_action_type_display()} -  {obj.target_group}'
        elif obj.action_type == 'new_interaction':
            return f'{obj.control_element} - {obj.get_action_type_display()}'
        return f'Неизвестный тип действия'


class ControlElementActionEditSerializer(serializers.ModelSerializer):
    control_element = serializers.PrimaryKeyRelatedField(queryset=ControlElement.objects.all(), required=False)
    task_template = serializers.PrimaryKeyRelatedField(queryset=TaskTemplate.objects.all(), allow_null=True, required=False)
    target_group = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), allow_null=True, required=False)
    queue = serializers.PrimaryKeyRelatedField(queryset=Queue.objects.all(), allow_null=True, required=False)
    executor = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), allow_null=True, required=False)
    executor_group = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), allow_null=True, required=False)
    controller_group = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), allow_null=True, required=False)
    observer_group = serializers.PrimaryKeyRelatedField(queryset=AccountsGroup.objects.all(), allow_null=True, required=False)
    task_outcome = serializers.PrimaryKeyRelatedField(queryset=ControlElement.objects.all(), allow_null=True, required=False)

    class Meta:
        model = ControlElementAction
        fields = '__all__'

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['editor'] = self.context['request'].user
        return super().update(instance, validated_data)

class TaskResultSerializer(serializers.ModelSerializer):
    task = ResultTaskSerializer(required=False)
    status_display = serializers.SerializerMethodField()
    outcome = ControlElementBaseSerializer(required=False)
    outcomes = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = TaskResult
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_str(self, obj):
        return f'{obj.task} - {obj.get_status_display()}'

    def get_outcomes(self, obj):
        outcomes = ControlElement.objects.filter(
            task_template=obj.task.task_template,
        )
        return ControlElementBaseSerializer(outcomes, many=True, context=self.context).data

class TaskResultEditSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)
    outcome = serializers.PrimaryKeyRelatedField(queryset=ControlElement.objects.all(), required=False, allow_null=True)

    class Meta:
        model = TaskResult
        fields = '__all__'

class PlanResultSerializer(serializers.ModelSerializer):
    task = ResultTaskSerializer(required=False)
    status_display = serializers.SerializerMethodField()
    outcome = ControlElementBaseSerializer(required=False)
    outcomes = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = PlanResult
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_str(self, obj):
        return f'{obj.task} - {obj.get_status_display()}'

    def get_outcomes(self, obj):
        outcomes = ControlElement.objects.filter(
            task_template=obj.task.task_template,
        )
        return ControlElementBaseSerializer(outcomes, many=True, context=self.context).data

class PlanResultEditSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)
    outcome = serializers.PrimaryKeyRelatedField(queryset=ControlElement.objects.all(), required=False, allow_null=True)

    class Meta:
        model = PlanResult
        fields = '__all__'

class MaterialResultSerializer(serializers.ModelSerializer):
    task = ResultTaskSerializer(required=False)
    status_display = serializers.SerializerMethodField()
    outcome = ControlElementBaseSerializer(required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = MaterialResult
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_str(self, obj):
        return f'{obj.task} - {obj.get_status_display()}'

class MaterialResultEditSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)
    outcome = serializers.PrimaryKeyRelatedField(queryset=ControlElement.objects.all(), required=False, allow_null=True)

    class Meta:
        model = MaterialResult
        fields = '__all__'

class NewResultSerializer(serializers.ModelSerializer):
    task = ResultTaskSerializer(required=False)
    status_display = serializers.SerializerMethodField()
    outcome = ControlElementBaseSerializer(required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = NewResult
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_str(self, obj):
        return f'{obj.task} - {obj.get_status_display()}'

class NewResultEditSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)
    outcome = serializers.PrimaryKeyRelatedField(queryset=ControlElement.objects.all(), required=False, allow_null=True)

    class Meta:
        model = NewResult
        fields = '__all__'


class CourseResultSerializer(serializers.ModelSerializer):
    task = ResultTaskSerializer(required=False)
    status_display = serializers.SerializerMethodField()
    outcome = ControlElementBaseSerializer(required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = CourseResult
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_str(self, obj):
        return f'{obj.task} - {obj.get_status_display()}'

class CourseResultEditSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)
    outcome = serializers.PrimaryKeyRelatedField(queryset=ControlElement.objects.all(), required=False, allow_null=True)

    class Meta:
        model = CourseResult
        fields = '__all__'

class TestResultBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = TestResult
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.task} - {obj.get_status_display()}'

class TestResultSerializer(serializers.ModelSerializer):
    task = ResultTaskSerializer(required=False)
    status_display = serializers.SerializerMethodField()
    outcome = ControlElementBaseSerializer(required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = TestResult
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_str(self, obj):
        return f'{obj.task} - {obj.get_status_display()}'

class TestResultEditSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)
    outcome = serializers.PrimaryKeyRelatedField(queryset=ControlElement.objects.all(), required=False, allow_null=True)

    class Meta:
        model = TestResult
        fields = '__all__'


class TestAttemptBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = TestAttempt
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.test_result.task.test.name} - {obj.number} - {obj.get_status_display()}'

class TestAttemptSerializer(serializers.ModelSerializer):
    test_name = serializers.SerializerMethodField()
    test_attempts = serializers.SerializerMethodField()
    test_result = TestResultBaseSerializer(required=False)
    status_display = serializers.SerializerMethodField()
    question_results = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = TestAttempt
        fields = '__all__'

    def get_test_name(self, obj):
        test_name = obj.test_result.task.test.name
        return test_name

    def get_test_attempts(self, obj):
        test_attempts = obj.test_result.task.test.attempts
        return test_attempts

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_question_results(self, obj):

        question_sorting = json.loads(obj.question_sorting)
        question_results = list(QuestionResult.objects.filter(
            test_attempt=obj,
            question_id__in=question_sorting
        ))
        question_results.sort(key=lambda qr: question_sorting.index(qr.question_id))

        return QuestionResultSerializer(question_results, many=True, context=self.context).data

    def get_str(self, obj):
        return f'{obj.test_result.task.test.name} - {obj.number} - {obj.get_status_display()}'

class QuestionResultSerializer(serializers.ModelSerializer):
    #test_attempt = TestAttemptBaseSerializer(required=False)
    question = QuestionSerializer(required=False)
    status_display = serializers.SerializerMethodField()
    answer_results = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = QuestionResult
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_answer_results(self, obj):
        test = obj.test_attempt.test_result.task.test
        if test.random_answers:
            answer_results = AnswerResult.objects.filter(question_result=obj).order_by('?')
        else:
            answer_results = AnswerResult.objects.filter(question_result=obj).order_by('answer__item')
        return AnswerResultSerializer(answer_results, many=True, context=self.context).data

    def get_str(self, obj):
        return f'{obj.question.text} | {obj.get_status_display()}'


class AnswerResultSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(required=False)
    status_display = serializers.SerializerMethodField()
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = AnswerResult
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_str(self, obj):
        return f'{obj.answer.text} | {obj.get_status_display()}'

class EventResultBaseSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = EventResult
        fields = '__all__'

    def get_str(self, obj):
        return f'{obj.task} - {obj.get_status_display()}'

class EventResultSerializer(serializers.ModelSerializer):
    task = ResultTaskSerializer(required=False)
    status_display = serializers.SerializerMethodField()
    outcome = ControlElementBaseSerializer(required=False)
    str = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField()
    editor = serializers.StringRelatedField()

    class Meta:
        model = EventResult
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_str(self, obj):
        return f'{obj.task} - {obj.get_status_display()}'

class EventResultEditSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)
    outcome = serializers.PrimaryKeyRelatedField(queryset=ControlElement.objects.all(), required=False, allow_null=True)

    class Meta:
        model = EventResult
        fields = '__all__'