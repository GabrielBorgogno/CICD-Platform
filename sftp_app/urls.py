from django.urls import path
from . import views

urlpatterns = [
    path('sftp_client/', views.sftp_client, name='sftp_client'),
    path('download_file/<str:file_name>/', views.download_file, name='download_file'),
]
