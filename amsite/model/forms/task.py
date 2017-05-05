from django.forms import ModelForm, BooleanField

from .. import Task


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'estimate']

    ready = BooleanField(required=False)
