from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Survey)
admin.site.register(SurveySection)
admin.site.register(SurveyQuestion)
admin.site.register(SurveySectionQuestion)
admin.site.register(SurveyAnswer)