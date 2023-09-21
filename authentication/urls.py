from django.urls import path
from .views import UserRegistrationView, UserLoginView , logout_view,  check_email_exists
from django.urls import path
from django.contrib.auth import views as auth_views




urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-registration"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path('logout/', logout_view, name='logout'),
    path('email-exists/', check_email_exists, name='email-exists'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



]
