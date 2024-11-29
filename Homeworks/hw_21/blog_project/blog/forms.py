from django import forms
from .models import Post, Tag


class PostForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        help_text="Select existing tags or create new ones."
    )

    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'category', 'tag']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
            'category': forms.Select(),
        }

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()

        # Handle dynamically created tags
        tags = self.cleaned_data['tag']
        for tag in tags:
            post.tag.add(tag)

        return post
