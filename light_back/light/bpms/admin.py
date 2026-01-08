from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Interaction)
admin.site.register(TaskTemplate)
admin.site.register(Task)
admin.site.register(PlanResult)
admin.site.register(TaskResult)
admin.site.register(NewResult)
admin.site.register(MaterialResult)
admin.site.register(CourseResult)
admin.site.register(EventResult)
admin.site.register(TestResult)
admin.site.register(TestAttempt)
admin.site.register(QuestionResult)
admin.site.register(AnswerResult)
admin.site.register(TaskTemplateAssignment)
admin.site.register(Queue)
admin.site.register(QueueTask)
admin.site.register(QueueExecutor)
admin.site.register(ControlElement)
admin.site.register(ControlElementEvent)
admin.site.register(ControlElementCondition)
admin.site.register(ControlElementAction)
admin.site.register(ControlElementActivation)





