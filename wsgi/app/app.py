from sys import exc_info
from urllib.parse import parse_qs
from datetime import timedelta

from .parse import get_dataset
from .utils import exc_parse, html_esc
from ..model import Task, Roadmap, State

DATASET_ENV = 'YML_DATASET'

default_headers = [
    ('Content-Type', 'text/html; charset=utf8'),
    ('Server', 'WSGIApplication/0.1'),
]

html_template = '''
<html>
 <head>
   <meta charset="utf-8"/>
 </head>
 <body>{}</body>
</html>
'''


class WSGIApplication:
    '''
    Simple WSGI-app that returns list of critical tasks
    from yaml dataset file.

    Environment variable `DATASET_ENV` contains filename.

    Params:
    - `days` (query argument) - number of days to limit tasks estimate. Default is 3
    - `state` (query argument) - in_progress|ready|any. Default in_progress
    '''

    @property
    def params(self):
        if not self._params:
            query_string = self.environment.get('QUERY_STRING', '')

            self._params = {
                key: value if len(value) > 1 else value[0]
                for key, value in parse_qs(query_string).items()
            }

        return self._params

    def __iter__(self):
        try:  # check if days is int and state allowed
            days = int(self.params.get('days', '3'))

            if self.params.get('state') != 'any':
                state = State(self.params.get('state', State.in_progress))
            else:
                state = None

        except ValueError:
            try: self.start_response('400 BAD REQUEST', [('Content-Type', 'text/plain')])
            except: pass
            yield html_esc('Wrong query param').encode()
            return

        try:
            self.start_response('200 OK', default_headers)

            # filter all tasks with given state that fits into `days` estimated range
            tasks = self._roadmap.filter(state) if state else self._roadmap.tasks
            critical = [
                task for task in tasks
                if task.remaining < timedelta(days)
            ]

            # format task representation into list and send
            response = html_template.format(
                '<br/>'.join([str(task) for task in critical])
            )

            yield response.encode()

        except:  # return 500 if any error during request
            traceback = '{} ({}) in <{}:{}>'.format(*exc_parse(exc_info()))
            try: self.start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'text/plain')])
            except: pass
            yield html_esc(traceback).encode()

    def __init__(self, environment, start_response_callback):
        self.environment = environment
        self.start_response = start_response_callback

        self._params = None
        self._roadmap = None

        try:
            tasks = []

            # parse dataset and fill roadmap with values
            for item in get_dataset(self.environment[DATASET_ENV]):
                tasks.append(Task(item[0], item[2]))
                if State(item[1]) == State.ready: tasks[-1].ready()

            self._roadmap = Roadmap(tasks)

        except ValueError:
            pass
