from django.urls import path
from . import views

urlpatterns = [
    # Your other URL patterns
    path('', views.home, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('user_data/', views.user_data, name='user_data'),
    path('diagram/', views.infra, name='infrastructure')

]
