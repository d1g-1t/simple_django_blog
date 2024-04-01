from django import forms
from django.contrib.auth.models import User

from blog.models import Category, Location, Post, Comment


class CategoryForm(forms.ModelForm):
    """
    Класс формы для категорий
    """
    class Meta:
        model = Category
        fields = '__all__'


class LocationForm(forms.ModelForm):
    """
    Класс формы для местоположений
    """
    class Meta:
        model = Location
        fields = '__all__'


class PostForm(forms.ModelForm):
    """
    Класс формы для публикаций
    """
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(
                format='%d/%m/%Y',
                attrs={'type': 'date'}
            )
        }


class CommentForm(forms.ModelForm):
    """
    Класс формы для комментариев
    """
    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):
    """
    Класс формы для пользователей
    """
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )
