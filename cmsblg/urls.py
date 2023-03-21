from django.urls import path
from . import views
from cmsblg.views import *

urlpatterns = [
    path('search/', views.search, name='search'),
    path('facts/', views.facts, name='facts'),
    path('createfact/', CreateFact.as_view(), name='createfaq'),
    path('UpdateFaq/<str:pk>', UpdateFaq.as_view(), name='UpdateFaq'),
    path('deletefaq/<str:pk>', views.deleteFaq, name='deletefaq'),
    path('categorycreateview/', CategoryCreateView.as_view(), name='categorycreateview'),
    path('<slug:category_slug>/<slug:slug>/', views.detail, name='post_detail'),
    path('<slug:slug>/', views.category, name='category_detail')
]