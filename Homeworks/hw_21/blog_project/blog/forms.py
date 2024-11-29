from django import forms
from .models import Post, Tag


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_tags'}),
        help_text="Enter tags separated by commas or add new ones dynamically."
    )

    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'category', 'tags']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Save the post instance, defer tag handling to the view
        post = super().save(commit=False)
        return post
