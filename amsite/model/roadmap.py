from typing import List

from datetime import date

from .task import Task
from .state import State

from django.db import models

from .uuid_model import UUIDModel


class Roadmap(UUIDModel):
    '''
    Defines filtered list of `Task`

    Params:
    - `title` - Roadmap name
    - `task_set` - QuerySet of tasks
    '''

    title = models.CharField()

    @property
    def today(self) -> List[Task]:
        '''
        Returns list of tasks whose estimated date is today
        '''
        return self.task_set.filter(estimate=date.today())

    def filter(self, state: State) -> List[Task]:
        '''
        Returns list of task with given state

        Args:
        - `state` - state of task
        '''
        return self.task_set.filter(state=state.value)
