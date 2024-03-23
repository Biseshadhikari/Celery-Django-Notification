# forms.py

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'desc']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border rounded-md p-2 w-full'}),
            'desc': forms.Textarea(attrs={'class': 'border rounded-md p-2 w-full h-32'}),
        }
