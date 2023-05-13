from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from auth_user.models import User

# Register your models here.
admin.site.register(User)