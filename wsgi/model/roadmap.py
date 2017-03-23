from typing import List

from datetime import date

from .task import Task
from .state import State


class Roadmap:
    '''
    Defines filtered list of `Task`

    Params:
    - `tasks` - list of all tasks
    '''

    tasks = property(lambda self: self.__tasks)

    @property
    def today(self) -> List[Task]:
        '''
        Returns list of tasks whose estimated date is today
        '''
        return [t for t in self.tasks if t.estimate == date.today()]

    def filter(self, state: State) -> List[Task]:
        '''
        Returns list of task with given state

        Args:
        - `state` - state of task
        '''
        return [t for t in self.tasks if t.state == state]

    def __init__(self, tasks: List[Task] = None) -> None:
        self.__tasks = tasks if tasks else []
