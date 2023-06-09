from django.urls import path, include
from . import views 
from cmscore.views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashabout/', dashabout, name='dashabout'),
    path('dashcmi/', dashcmi, name='dashcmi'),
    path('dashslider/', dashslider, name='dashslider'),
    path('dashfaq/', dashfaq, name='dashfaq'),
    path('dashcommodity/', dashcommodity, name='dashcommodity'),
    path('dashcommunity/', dashcommunity, name='dashcommunity'),
    path('dashproject/', dashproject, name='dashproject'),
    path('dashservices/', dashservices, name='dashservices'),
    path('dashuser/', dashuser, name='dashuser'),
    path('map/', map, name='map'),
    path('slider/', dashslider, name='slider'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('gallery/', gallery, name='gallery'),
    path('createalbum/', createalbum, name='createalbum'),
    path('albumupdate/<str:pk>/update/', albumupdate.as_view(), name='albumupdate'),
    path('deletealbum/<str:pk>/', deleteAlbum, name='deletealbum'),
    path('album/<str:pk>/', album, name='album'),
    path('createphoto/', createphoto, name='createphoto'),
    path('photoupdate/<str:pk>/update/', photoupdate.as_view(), name='photoupdate'),
    path('deletephoto/<str:pk>/', deletePhoto, name='deletephoto'),
    path('gallerysection/', galleryman, name='galleryman'),
    # path('photo/<str:pk>/', photo, name='photo'),
    path('createslide/', createslide, name='createslide'),
    path('deleteslide/<int:id>/', deleteslide, name='deleteslide'),
    path('slide/<str:pk>/update/', SliderUpdate.as_view(), name='sliderupdate'),
    path('consortium/', consortium, name='consortium'),
    path('createconsortium/', createconsortium, name='createconsortium'),
    path('consortium/<str:pk>/update/', ConsortiumUpdateView.as_view(), name='consortium_update'),
    path('organization/', organization, name='organization'),
    path('organizationcreateview/', OrganizationCreateView.as_view(), name='organizationcreateview'),
    path('organization/<str:pk>/update/', OrganizationUpdateView.as_view(), name='organization_update'),
    path('deleteorganization/<str:pk>/', deleteorganization, name='deleteorganization'),
    path('cmi/', cmi, name='cmi'),  
    path('cmidetail/', cmidetail, name='cmidetail'),  
    path('community/', community, name='community'),
    path('allpost/', allpost, name='allpost'),
    path('mypost/', mypost, name='mypost'),
    path('postsection/', postman, name='postman'), 
    path('postcreateview/', PostCreateView.as_view(), name='postcreateview'),
    path('mypost/<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('deleteuser/<int:id>/', deleteuser, name='deleteuser'),
    path('deletepost/<slug:slug>/', deletepost, name='deletepost'),
    path('deletecategory/<slug:slug>/', deletecategory, name='deletecategory'), 
    path('commodities/', commodities, name='commodities'),
    path('commodities/<slug:commodity_slug>/', commodetail, name='commodetail'),
    # path('commoditylist/', commoditylist.as_view(), name='commoditylist'),
    path('commoditycreateview/', CommodityCreateView.as_view(), name='commoditycreateview'),
    path('commodity/<slug:slug>/update/', CommodityUpdateView.as_view(), name='commodity_update'),
    path('deletecommodity/<slug:commodity_slug>/', deletecommodity, name='deletecommodity'),
    path('projects/', project, name='project'),
    path('onprojects/', onproject, name='onproject'),
    path('finprojects/', finproject, name='finproject'),
    path('projectcreateview/', ProjectCreateView.as_view(), name='projectcreateview'),
    path('onprojects/<slug:project_slug>/', onprojectdetail, name='onprojectdetail'),
    path('finprojects/<slug:project_slug>/', finprojectdetail, name='finprojectdetail'),
    path('project/<slug:slug>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('deleteproject/<slug:project_slug>/', projectdelete, name='projectdelete'),
    path('services/', services, name='services'),
]