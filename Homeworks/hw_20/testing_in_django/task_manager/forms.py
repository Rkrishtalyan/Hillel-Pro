from django import forms
from django.utils import timezone


# ---- Task Form Definition ----
class TaskForm(forms.Form):
    """
    Represent a form for creating or editing a task.

    The form includes fields for task title, description, and due date,
    and validates that the due date is not in the past.

    :var title: The title of the task.
    :type title: forms.CharField
    :var description: The description of the task.
    :type description: forms.CharField
    :var due_date: The due date of the task.
    :type due_date: forms.DateField
    """

    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    due_date = forms.DateField(widget=forms.DateInput, required=False)

    def clean_due_date(self):
        """
        Validate the due date to ensure it is not in the past.

        :return: The cleaned due date.
        :rtype: date
        :raises forms.ValidationError: If the due date is in the past.
        """
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError("Due date cannot be in the past.")
        return due_date
