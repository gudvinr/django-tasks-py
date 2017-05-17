import uuid
from datetime import date

from django.db import models

from .state import State
from .user import User


class Roadmap(models.Model):
    '''
    Defines filtered list of `Task`

    Params:
    - `title` - Roadmap name
    - `task_set` - QuerySet of tasks
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=256)

    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, blank=False)

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
