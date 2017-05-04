from django.forms import ModelForm
from django.db import models

from .. import Task


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'estimate']

    ready = models.BooleanField()
