# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib.auth.models import User, auth
# from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.urls import reverse
# from django.contrib.auth import authenticate, login as auth_login, logout


# # def register(request):
# #     if request.method == 'POST':
# #         username = request.POST['username']
# #         email = request.POST['email']
# #         password = request.POST['password']
# #         password2 = request.POST['password2']

# #         if password == password2:
# #             if User.objects.filter(email=email).exists():
# #                 messages.info(request, 'Email already used')
# #                 return redirect('register')
# #             elif User.objects.filter(username=username).exists():
# #                 messages.info(request, 'Username already used')
# #                 return redirect('register')

# #             else:
# #                 user = User.objects.create_user(username=username, email=email, password=password)  
# #                 user.save(); 
# #                 return redirect('login')
# #         else:
# #             messages.info(request, 'Password is not the same')
# #             return redirect('register')
# #     else:
# #         return render(request, 'registration/register.html')


# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
        
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             auth_login(request, user)
#             return redirect('index')
#         else:
#             messages.error(request, 'Invalid Credentials')
#             return render(request, 'registration/login.html')
            
#     else:
#         return render(request, 'registration/login.html')


# def logout(request):
#     logout(request)
#     return redirect('/')
