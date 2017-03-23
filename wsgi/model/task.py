from typing import Union

from datetime import datetime as dt, timedelta, date

from .state import State


class Task:
    ''' This class provides model for Task

    Params:
    - `title` - name of the Task
    - `estimate` - last day of the Task

    Representation:
    `title: estimate (remaining)`
    '''

    title = property(lambda self: self.__title)
    state = property(lambda self: self.__state)
    estimate = property(lambda self: self.__estimate)

    @title.setter
    def title(self, title: str) -> None:
        self.__title = title

    @estimate.setter
    def estimate(self, estimate: date) -> None:
        '''
        Sets new estimate value.

        Raises:
        `ValueError` if estimate earlier than today
        '''
        if estimate < date.today(): raise ValueError('New estimate value should be at least today')

        self.__estimate: date = estimate

    @property
    def remaining(self) -> timedelta:
        ''' Returns days left to estimate date or zero `timedelta` if ready '''
        if self.state == State.in_progress:
            return self.estimate - date.today()
        else:
            return timedelta()

    @property
    def is_failed(self) -> bool:
        ''' Returns true if task state `is_running` and `remaining < 0` '''
        return self.state == State.in_progress and self.estimate < date.today()

    def ready(self) -> bool:
        '''
        Switches state to ready

        Returns:
        `false` if already done
        '''

        s = self.state
        self.__state = State.ready
        return self.state != s

    def __str__(self) -> str:
        return "{}: {} ({})".format(
            self.title,
            self.estimate.strftime('%Y-%m-%d'),
            self.remaining.days if not self.state == State.ready else '✓'
        )

    def __init__(self, title: str, estimate: Union[date, str]) -> None:
        self.__title = title

        self.__estimate = dt.strptime(estimate, '%Y-%m-%d').date() if type(estimate) == str else estimate  # noqa

        self.__state = State.in_progress
