from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path('', include('frontend.urls')),
    path('', include('devops.urls')),
    path('', include('sftp_app.urls')),



]
