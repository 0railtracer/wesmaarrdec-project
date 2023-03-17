from django.urls import path, include
from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path("verification/", views.verification_sent, name="verification_sent"),
    path("registercustom/", views.registercustom, name="registercustom"),

]