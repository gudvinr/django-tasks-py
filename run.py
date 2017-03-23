import os
from wsgi.app import WSGIApplication, DATASET_ENV

os.environ[DATASET_ENV] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dataset.yml')

from wsgiref.simple_server import make_server  # noqa

with make_server('127.0.0.1', 9090, WSGIApplication) as http_server:
    http_server.serve_forever()
