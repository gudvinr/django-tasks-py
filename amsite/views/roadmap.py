from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Sum
from django.views import View
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.urls import reverse

from amsite.models import Roadmap, Task, State, forms


class RoadmapView(LoginRequiredMixin, View):

    def post(self, request, id=None):
        '''Add new task'''

        try:
            rm = Roadmap.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({'ok': False, 'error': "Roadmap {} not found".format(id)})

        new_ts = Task(roadmap=rm)
        form = forms.TaskForm(request.POST, instance=new_ts)

        if not form.is_valid(): return JsonResponse({'ok': False, 'error': str(form.errors)})

        new_ts = form.save()
        return JsonResponse({
            'ok': True,
            'result': {
                '_url': reverse('task', args=[id, new_ts.id]),
                **model_to_dict(new_ts)
            }
        })

    def delete(self, request, id=None):
        '''Delete Roadmap'''

        try:
            rm = Roadmap.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({'ok': False, 'error': "Roadmap {} not found".format(id)})

        if rm.delete()[0] == 0: return JsonResponse({'ok': False, 'error': "Can't delete"})
        return JsonResponse({'ok': True})

    def get(self, request, id=None):
        ''' Used to render list of task '''

        try:
            rm = Roadmap.objects.get(id=id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

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

        return render(request, 'roadmap.html', payload)


class RoadmapStatView(LoginRequiredMixin, View):

    def get(self, request, id=None):
        ''' Returns json with stat data '''
        try:
            rm = Roadmap.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({'ok': False, 'error': "Can't find roadmap with id {}".format(id)})

        # FIXME: we shouldn't put hardcoded table names and columns here in extra
        tasks = Task.objects.select_related('score').filter(roadmap=rm, state=State.ready.value) \
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
        ts_weekly = Task.objects.filter(roadmap=rm) \
            .extra({
                'created_week': "strftime('%%W', created)",
                'created_year': "strftime('%%Y', created)"
            }) \
            .values('created_year', 'created_week') \
            .annotate(total=Count('id'))

        ts_weekly_done = tasks.values('completed_year', 'completed_week').annotate(done=Count('id'))

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
