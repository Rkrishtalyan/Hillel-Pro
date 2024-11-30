# ---- Import Statements ----
from django import forms

from .models import Post


# ---- Form Definitions ----

class PostForm(forms.ModelForm):
    """
    Define a form for the Post model with additional handling for tags.

    :var tags: A custom field for tags, allowing comma-separated input.
    """

    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_tags'}),
        help_text="Enter tags separated by commas or add new ones dynamically."
    )

    class Meta:
        """
        Meta options for the PostForm.

        :var model: The model to associate with the form.
        :var fields: The fields to include in the form.
        :var widgets: Custom widgets for specific fields.
        """
        model = Post
        fields = ['title', 'body', 'image', 'category', 'tags']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        """
        Save the Post instance with deferred tag handling.

        :param commit: Whether to commit the save immediately.
        :type commit: bool
        :return: The saved or unsaved Post instance.
        :rtype: Post
        """
        post = super().save(commit=False)
        return post
