# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import UploadResumeAPIView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('resume/', UploadResumeAPIView.as_view(), name='upload_resume'),
]
