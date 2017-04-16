from datetime import date

from django.db import models

from .state import State
from .uuid_model import UUIDModel


class Roadmap(UUIDModel, models.Model):
    '''
    Defines filtered list of `Task`

    Params:
    - `title` - Roadmap name
    - `task_set` - QuerySet of tasks
    '''

    title = models.CharField(max_length=256)

    @property
    def today(self) -> list:
        '''
        Returns list of tasks whose estimated date is today
        '''
        return self.task_set.filter(estimate=date.today())

    def filter(self, state: State) -> list:
        '''
        Returns list of task with given state

        Args:
        - `state` - state of task
        '''
        return self.task_set.filter(state=state.value)
