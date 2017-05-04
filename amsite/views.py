from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.forms.models import model_to_dict

from .model import Roadmap, Task, State
from .model.forms import RoadmapForm, TaskForm


def index(request):
    return render(request, 'index.html')


def roadmaps(request):
    if request.method == 'POST':
        form = RoadmapForm(request.POST)

        if not form.is_valid(): return JsonResponse({'ok': False, 'error': str(form.errors)})

        new_rm = form.save()
        return JsonResponse({
            'ok': True,
            'result': {
                '_url': reverse('roadmap', args=[new_rm.id]),
                **model_to_dict(new_rm)
            }
        })

    payload = {
        'roadmaps': Roadmap.objects.all().values()
    }

    return render(
        request, 'roadmaps.html', payload
    )


def roadmap(request, id=None):
    rm = Roadmap.objects.get(id=id)

    if request.method == 'POST':
        new_ts = Task(roadmap=rm)
        form = TaskForm(request.POST, instance=new_ts)

        if not form.is_valid(): return JsonResponse({'ok': False, 'error': str(form.errors)})

        new_ts = form.save()
        return JsonResponse({
            'ok': True,
            'result': {
                '_url': reverse('task', args=[id, new_ts.id]),
                **model_to_dict(new_ts)
            }
        })

    tasks = Task.objects.filter(roadmap=rm)
    tasks = [{
        **model_to_dict(ts),
        'ready': ts.state == State.ready.value,
        'is_failed': ts.is_failed,
        'id': ts.id
    } for ts in tasks]

    payload = {
        'id': id,
        'tasks': tasks,
        **model_to_dict(rm)
    }

    return render(
        request, 'roadmap.html', payload
    )


def task(request, roadmap=None, id=None):
    ts = Task.objects.get(id=id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=ts)

        if not form.is_valid(): return JsonResponse({'ok': False, 'error': str(form.errors)})

        if form.ready: ts.ready()

        ts = form.save()
        return JsonResponse({'ok': True, 'result': model_to_dict(ts)})

    payload = {
        'id': ts.id,
        'ready': ts.state == State.ready.value,
        **model_to_dict(ts),
        'roadmap': {
            'id': ts.roadmap.id,
            **model_to_dict(ts.roadmap)
        }
    }

    return render(
        request, 'task.html', payload
    )
