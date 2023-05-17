from django.conf.urls import url
from AnalysisApp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[    
    url(r'^polen/$', views.polenApi),
    url(r'^polen/([0-9]+)$', views.polenApi),
    url(r'^uploadVSI/$', views.uploadVSI),
    url(r'^analyse/$', views.analyseSelectedImages),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)