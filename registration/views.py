from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from .models import VerificationToken

# def send_verification_email(request, user, verification_token):
#     subject = 'Verify your email address'
#     message = render_to_string('verification_email.html', {
#         'user': user,
#         'verification_token': verification_token,
#         'domain': request.META['HTTP_HOST'],
#     })
#     plain_message = strip_tags(message)
#     from_email = 'Your Company <noreply@yourcompany.com>'
#     recipient_list = [user.email]
#     send_mail(subject, plain_message, from_email, recipient_list, html_message=message)

# def verify(request, token):
#     try:
#         verification_token = VerificationToken.objects.get(token=token)
#         user = verification_token.user
#         user.is_active = True
#         user.save()
#         verification_token.delete()
#         return HttpResponse('Your account has been verified. You can now log in.')
#     except VerificationToken.DoesNotExist:
#         return HttpResponse('Invalid verification token.')
    

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()

#             verification_token = VerificationToken.objects.create(user=user)
#             token = verification_token.token

#             # Send verification email
#             subject = 'Verify your account'
#             message = render_to_string('registration/email_verification.html', {
#                 'user': user,
#                 'token': token,
#                 'domain': request.META['HTTP_HOST']
#             })
#             plain_message = strip_tags(message)
#             from_email = 'Your Company <noreply@yourcompany.com>'
#             recipient_list = [user.email]
#             send_mail(subject, plain_message, from_email, recipient_list, html_message=message)

#             return redirect('verification_sent')
#     else:
#         form = UserCreationForm()
#     return render(request, 'users/register.html', {'form': form})

# def verification_sent(request):
#     return render(request, 'registration/verification_sent.html')
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used')
                return redirect('register')

            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save(); 
                return redirect('login')
        else:
            messages.info(request, 'Password is not the same')
            return redirect('register')
    else:
        return render(request, 'registration/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'registration/login.html', {'messages': messages})

def logout(request):
    auth.logout(request)
    return redirect('/')

def registercustom(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))