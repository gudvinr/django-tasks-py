from enum import Enum, auto


class AutoName(Enum):

    def _generate_next_value_(name, start, count, last_values):  # noqa
        return name


class State(AutoName):
    '''
    Enum that defines possible states of Task
    '''

    in_progress = auto()
    ready = auto()
