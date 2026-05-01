# from django.contrib import admin
from django.urls import path
# from rest_framework.routers import DefaultRouter
from .views import UploadFileView


# /upload/file

urlpatterns = [
    path("file",UploadFileView.as_view()),
    
]