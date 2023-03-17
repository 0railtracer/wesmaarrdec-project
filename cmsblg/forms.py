from django import forms

from .models import Comment, Category, Fact

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', )

class FactForm(forms.ModelForm):
    class Meta:
        model = Fact
        fields = '__all__'