# your_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('scripts/', views.list_remote_files, name='scripts'),
    path('execute_script/', views.execute_script, name='execute_script'),
    path('migration/', views.migration_monitor, name='migration_monitor'),

]


