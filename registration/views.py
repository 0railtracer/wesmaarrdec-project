from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from cmscore.models import Loginbg
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from auth_user.models import User
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    loginbg = get_object_or_404(Loginbg)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid Credentials!')
            return redirect('login')
    else:
        
        return render(request, 'registration/login.html', {'loginbg': loginbg})

def logout_view(request):
    logout(request)
    return redirect('/')

# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password2 = request.POST['password2']

#         if password == password2:
#             if User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email already used')
#                 return redirect('register')
#             elif User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username already used')
#                 return redirect('register')

#             else:
#                 user = User.objects.create_user(username=username, email=email, password=password)  
#                 user.save(); 
#                 return redirect('login')
#         else:
#             messages.info(request, 'Password is not the same')
#             return redirect('register')
#     else:
#         return render(request, 'registration/register.html')

# def registercustom(request):
#     if request.method == "GET":
#         return render(
#             request, "users/register.html",
#             {"form": CustomUserCreationForm}
#         )
#     elif request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect(reverse("dashboard"))