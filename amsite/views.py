import datetime as dt

from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Sum

from .model import Roadmap, Task, State, Scores
from .model.forms import RoadmapForm, TaskForm


def index(request):
    ''' Placeholder '''
    return render(request, 'index.html')


def roadmaps(request):
    ''' Returns page with list of roadmaps or creates new one '''

    if request.method == 'POST':
        # Create roadmap

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
    ''' Used to render list of task and add new tasks to roadmap '''

    try:
        rm = Roadmap.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == 'POST':
        # Add new task

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
    elif request.method == 'DELETE':
        # Delete Roadmap

        if rm.delete()[0] == 0: return JsonResponse({'ok': False, 'error': "Can't delete"})
        return JsonResponse({'ok': True})

    # Make roadmap template
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


def rm_stat(request, id=None):
    ''' Returns json with stat data '''
    try:
        rm = Roadmap.objects.get(id=id)
    except ObjectDoesNotExist:
        return JsonResponse({'ok': False, 'error': "Can't find roadmap with id {}".format(id)})

    # FIXME: we shouldn't put hardcoded table names and columns here in extra
    tasks = Task.objects.select_related('score').filter(roadmap=rm) \
        .extra({
            'created_week': "strftime('%%W', created)",
            'created_year': "strftime('%%Y', created)"
        }) \
        .extra(
            select={
                'completed_week': "strftime('%%W', amsite_scores.date)",
                'completed_year': "strftime('%%Y', amsite_scores.date)",
                'completed_month': "strftime('%%m', amsite_scores.date)"
            },
            where=('amsite_task.id=amsite_scores.task_id',),
            tables=('amsite_scores',)
    )

    # Group tasks by weeks
    ts_weekly = tasks \
        .values('created_year', 'created_week') \
        .annotate(total=Count('id'))

    ts_weekly_done = tasks \
        .filter(state=State.ready.value) \
        .values('completed_year', 'completed_week') \
        .annotate(done=Count('id'))

    # Make single list
    for ts_t in ts_weekly:
        ts_t['done'] = sum([
            t['done'] for t in ts_weekly_done
            if t['completed_week'] == ts_t['created_week'] and t['completed_year'] == ts_t['created_year']
        ])

        ts_t['week'] = ts_t.pop('created_week')
        ts_t['year'] = ts_t.pop('created_year')

    # Group tasks by month with points
    ts_monthly = tasks.values('completed_year', 'completed_month').annotate(scores=Sum('score__points'))

    for t in ts_monthly:
        t['month'] = t.pop('completed_month')
        t['year'] = t.pop('completed_year')

    return JsonResponse({
        'ok': True,
        'result': {
            # 'stat': [model_to_dict(t.score) for t in tasks],
            'weekly': list(ts_weekly),
            'monthly': list(ts_monthly)
        }
    })


def task(request, roadmap=None, id=None):
    ''' Query and save task '''

    try:
        ts = Task.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == 'POST':
        # Edit task

        form = TaskForm(request.POST, instance=ts)

        if not form.is_valid(): return JsonResponse({'ok': False, 'error': str(form.errors)})

        if form.cleaned_data['ready']:
            ts.ready()
            ts = form.save()

            # Create scores record if task is ready
            Scores(date=dt.date.today(), task=ts).save()
        else:
            ts = form.save()

        return JsonResponse({'ok': True, 'result': model_to_dict(ts)})

    elif request.method == 'DELETE':
        # Delete task

        if ts.delete()[0] != 1: return JsonResponse({'ok': False, 'error': "Can't delete"})
        return JsonResponse({'ok': True})

    # Returns template if GET is processed
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
