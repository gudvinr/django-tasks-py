# from typing import Union

from datetime import timedelta, date
from django.db import models

from .uuid_model import UUIDModel
from .roadmap import Roadmap
from .state import State


class Task(UUIDModel, models.Model):
    ''' This class provides model for Task

    Params:
    - `title` - name of the Task
    - `estimate` - last day of the Task

    Representation:
    `title: estimate (remaining)`
    '''

    title = models.CharField(max_length=256)
    state = models.CharField(max_length=32, default=State.in_progress.value)
    estimate = models.DateField()
    created = models.DateField(default=date.today, editable=False)

    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)

    @property
    def remaining(self) -> timedelta:
        ''' Returns days left to estimate date or zero `timedelta` if ready '''
        if State(self.state) == State.in_progress:
            return self.estimate - date.today()
        else:
            return timedelta()

    @property
    def is_failed(self) -> bool:
        ''' Returns true if task state `is_running` and `remaining < 0` '''
        return State(self.state) == State.in_progress and self.estimate < date.today()

    def ready(self) -> bool:
        '''
        Switches state to ready

        Returns:
        `false` if already done
        '''

        s = State(self.state)
        self.state = State.ready.value
        return State(self.state) != s

    def __str__(self) -> str:
        return "{}: {} ({})".format(
            self.title,
            self.estimate.strftime('%Y-%m-%d'),
            self.remaining.days if not State(self.state) == State.ready else '✓'
        )
