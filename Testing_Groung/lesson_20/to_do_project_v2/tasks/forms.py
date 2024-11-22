from django import forms


class TaskForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    due_date = forms.DateField(widget=forms.DateInput, required=False)
