from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def about_view(request):
    return render(request, 'about.html')

@login_required
def contact_view(request):
    return render(request, 'contact.html')

@login_required
def user_data(request):
    return render(request, 'user_data.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def infra(request):
    return render(request, 'infra.html')
