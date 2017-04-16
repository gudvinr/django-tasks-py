import datetime as dt

# from django.http import HttpResponseNotFound
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def roadmaps(request):
    return render(
        request, 'roadmaps.html',
        {
            'roadmaps': [
                {'id': '123e4567-e89b-12d3-a456-426655440000', 'title': 'Title'}
            ]
        }
    )


def roadmap(request, id=None):
    id = '123e4567-e89b-12d3-a456-426655440000'
    title = 'Title'

    tasks = [{'id': '123e4567-e89b-12d3-a456-426655440000', 'title': 'Task title'}]

    return render(
        request, 'roadmap.html',
        {
            'id': id,
            'title': title,
            'tasks': tasks
        }
    )


def task(request, roadmap=None, id=None):
    id = '123e4567-e89b-12d3-a456-426655440000'
    title = 'Task title'

    roadmap = {'id': '123e4567-e89b-12d3-a456-426655440000', 'title': 'Title'}

    return render(
        request, 'task.html',
        {
            'roadmap': roadmap,
            'id': id,
            'title': title,
            'estimate': dt.date.today(),
            'roadmap': roadmap
        }
    )
