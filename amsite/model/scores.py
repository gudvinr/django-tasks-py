import uuid
import datetime as dt

from django.db import models

from .task import Task


class Scores(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    date = models.DateField()
    points = models.IntegerField()

    task = models.OneToOneField(Task)

    def calc_points(self):
        task = self.task
        return (
            (dt.date.today() - task.created) /
            (task.estimate - task.created)
        ) + (
            (task.estimate - task.created) /
            (1)  # TODO: fetch max value
        )

    def save(self, *args, **kwargs):
        self.points = self.calc_points()

        super().save(*args, **kwargs)