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
        post = super().save(commit=False)
        if commit:
            post.save()

        # Handle tags
        tag_string = self.cleaned_data['tags']
        tag_list = [tag.strip() for tag in tag_string.split(',') if tag.strip()]
        post.tag.clear()  # Clear existing tags
        for tag_name in tag_list:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            post.tag.add(tag)

        return post
