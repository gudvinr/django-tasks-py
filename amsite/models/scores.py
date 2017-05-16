import uuid
import datetime as dt

from django.db import models
from django.db.models import F, Max, ExpressionWrapper, DurationField

from .task import Task


class Scores(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    date = models.DateField()
    points = models.IntegerField()

    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='score')

    def calc_points(self):
        task = self.task

        max_est = Task.objects.all().aggregate(
            max_est=ExpressionWrapper(Max(F('estimate') - F('created')), output_field=DurationField())
        )['max_est']

        if not max_est: max_est = (task.estimate - task.created)

        return (
            (dt.date.today() - task.created) / (task.estimate - task.created)
        ) + (
            (task.estimate - task.created) / (max_est)
        )

    def save(self, *args, **kwargs):
        self.points = self.calc_points()

        super().save(*args, **kwargs)
