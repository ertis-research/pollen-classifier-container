from rest_framework import serializers
from AnalysisApp.models import Polen

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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
        
class PolenTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['username'] = user.username
        token['email'] = user.email
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Add extra responses here
        # data['username'] = self.user.username
        # data['email'] = self.user.email
                
        return data

class PolenTokenObtainPairView(TokenObtainPairView):
    serializer_class = PolenTokenObtainPairSerializer