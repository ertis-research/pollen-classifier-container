from rest_framework import serializers
from AnalysisApp.models import Polen

class PolenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polen
        fields = ('AnalysisId',
                  'UserId',
                  'AnalysisName',
                  'AnalysisDate',
                  'SampleDate',
                  'PhotoFileName',
                  'PhotoFilePath',
                  'AnalysisResult')

