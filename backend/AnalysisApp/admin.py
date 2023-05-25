from django.contrib import admin
from django.contrib.admin import ModelAdmin

# Register your models here.

from AnalysisApp.models import Polen

class PolenAdmin(ModelAdmin):
    list_display = ('AnalysisId', 'UserId', 'AnalysisName', 'AnalysisDate', 'SampleDate', 'PhotoFileName', 'PhotoFilePath', 'AnalysisResult')

admin.site.register(Polen, PolenAdmin)
