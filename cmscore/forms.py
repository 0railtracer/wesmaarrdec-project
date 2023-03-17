from django.forms import ModelForm
from django import forms
from .models import *
from cmsblg.models import *
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'intro', 'body', 'image']
        labels = {
            'title': 'Title',
            'category': 'Category',
            'intro': 'Introduction',
            'body': 'Body',
            'image': 'Image'
        }
    
class ConsortiumForm(ModelForm):
    class Meta:
        model = Consortium
        fields = '__all__'
        labels = '__all__'
        
class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['title', 'name', 'detail', 'image1', 'image2', ]
        labels = {
            'title': 'Title',
            'name': 'Name',
            'detail': 'Detail',
            'image1': 'Image1',
            'image2': 'Image2',
        }

class CommodityForm(ModelForm):
    class Meta:
        model = Commodity
        fields = ['name', 'detail', 'image']
        labels = {
            'name': 'Name',
            'detail': 'Detail',
            'image': 'Image',
        }

class SlideForm(ModelForm):
    class Meta:
        model = Slide
        fields = '__all__'

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'researcher', 'image1', 'image2', 'status']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'researcher': 'Researcher',
            'status': 'Status',
            'image1': 'Image1',
            'image2': 'Image2',
        }

class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = '__all__'
        labels = '__all__'

class PhotoForm(forms.ModelForm):
    class Meta:
        model = AlbumPhoto
        fields = '__all__'
        labels = '__all__'
        widgets = {
                'slide': forms.CheckboxInput(),
                'carousel': forms.CheckboxInput(),
        }