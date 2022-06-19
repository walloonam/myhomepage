from .models import *
from django import forms
from django.forms import ModelForm
from .forms import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
