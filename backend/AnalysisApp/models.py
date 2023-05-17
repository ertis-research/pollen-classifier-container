from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Polen(models.Model):
    AnalysisId = models.AutoField(primary_key=True)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)    
    AnalysisName = models.CharField(max_length=100)
    AnalysisDate = models.DateField()
    SampleDate = models.DateField()
    PhotoFileName = models.CharField(max_length=200)
    PhotoFilePath = models.CharField(max_length=200)
    AnalysisResult = models.JSONField()