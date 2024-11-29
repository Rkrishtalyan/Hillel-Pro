from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'tag', 'is_active']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
            'category': forms.CheckboxSelectMultiple(),
            'tag': forms.CheckboxSelectMultiple(),
        }
