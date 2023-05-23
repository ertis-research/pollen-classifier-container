from django.urls import re_path
from AnalysisApp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[    
    re_path(r'^polen/$', views.polenApi),
    re_path(r'^polen/([0-9]+)$', views.polenApi),
    re_path(r'^uploadVSI/$', views.uploadVSI),
    re_path(r'^analyse/$', views.analyseSelectedImages),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)