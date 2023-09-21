from django.shortcuts import redirect, render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import login
from django.views.generic import TemplateView
from rest_framework.renderers import TemplateHTMLRenderer
from django.urls import reverse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .backends import CustomAuthenticationBackend
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib.auth.models import User
from django.core.cache import cache



def logout_view(request):
    logout(request)
    # Redirect to a specific URL or any other view after logout (optional)
    return redirect('home')  # Change 'home' to the URL name you want to redirect to


def check_email_exists(request):
    email = request.GET.get('email')
    User = get_user_model()
    email_exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': email_exists})

class UserRegistrationView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registration.html'

    def get(self, request):
        serializer = UserSerializer()
        return Response({'serializer': serializer})

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Get the username and password from the serializer
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            # Authenticate the user using the custom backend
            user = CustomAuthenticationBackend().authenticate(request, email=email, password=password)

            if user is not None:
                # Armazene o token no cache do Redis
                cache.set('token', user.token, timeout=3600)  # 3600 segundos = 1 hora

                login(request, user)
                home_url = reverse('home')  # Assuming 'home' is the name of the URL pattern for the home page in your other microservice
                return redirect(home_url)
            else:
                return Response({"message": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return render(request, self.template_name, {'serializer': serializer})

# views.py
 # Replace 'dashboard.html' with your actual dashboard template path

def get_cached_token():
       token = cache.get('token')
       if token is not None:
           # Token encontrado no cache
           print(token)
           return token
       else:
           # Token não encontrado no cache
           return None   
       
class UserLoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def get(self, request):
        serializer = LoginSerializer()
        return Response({'serializer': serializer})

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Get the username and password from the serializer
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            # Authenticate the user using the custom backend
            user = CustomAuthenticationBackend().authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                home_url = reverse('home')  # Assuming 'home' is the name of the URL pattern for the home page in your other microservice
                return redirect(home_url)
            else:
                return Response({"message": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return render(request, self.template_name, {'serializer': serializer})


