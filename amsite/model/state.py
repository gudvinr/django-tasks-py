from enum import Enum


class State(Enum):
    '''
    Enum that defines possible states of Task
    '''

    in_progress = 'in_progress'
    ready = 'ready'
