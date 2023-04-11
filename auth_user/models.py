from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    researcher= models.BooleanField(default=False)
    secretariat= models.BooleanField(default=False)
    stakeholder= models.BooleanField(default=False)
