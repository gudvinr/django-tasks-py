import datetime as dt

from django.http import JsonResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.forms.models import model_to_dict
from django.shortcuts import render

from amsite.model import Task, Scores, State, forms


class TaskView(View):

    def post(self, request, roadmap=None, id=None):
        ''' Edit task '''

        try:
            ts = Task.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({'ok': False, 'error': "Can't find task {}".format(id)})

        form = forms.TaskForm(request.POST, instance=ts)

        if not form.is_valid(): return JsonResponse({'ok': False, 'error': str(form.errors)})

        if form.cleaned_data['ready']:
            ts.ready()
            ts = form.save()

            # Create scores record if task is ready
            Scores(date=dt.date.today(), task=ts).save()
        else:
            ts = form.save()

        return JsonResponse({'ok': True, 'result': model_to_dict(ts)})

    def delete(self, request, roadmap=None, id=None):
        ''' Delete task '''

        try:
            ts = Task.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({'ok': False, 'error': "Can't find task {}".format(id)})

        if ts.delete()[0] != 1: return JsonResponse({'ok': False, 'error': "Can't delete"})
        return JsonResponse({'ok': True})

    def get(self, request, roadmap=None, id=None):
        ''' Query and save task '''

        try:
            ts = Task.objects.get(id=id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

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

        return render(request, 'task.html', payload)
