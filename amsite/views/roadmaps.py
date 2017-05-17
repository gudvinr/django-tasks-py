from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.urls import reverse

from ..models import Roadmap, forms


class RoadmapsView(LoginRequiredMixin, View):

    def post(self, request):
        ''' Create roadmap '''

        form = forms.RoadmapForm(request.POST)

        if not form.is_valid(): return JsonResponse({'ok': False, 'error': str(form.errors)})

        new_rm = form.save(commit=False)
        new_rm.author = request.user
        new_rm.save()

        return JsonResponse({
            'ok': True,
            'result': {
                '_url': reverse('roadmap', args=[new_rm.id]),
                **model_to_dict(new_rm)
            }
        })

    def get(self, request):
        ''' Returns page with list of roadmaps '''

        payload = {
            'roadmaps': Roadmap.objects.filter(author=request.user).values()
        }

        return render(request, 'roadmaps.html', payload)
