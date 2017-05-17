from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse

from amsite.models import User


class ProfileView(LoginRequiredMixin, View):

    def post(self, request, id=None):
        ''' Edit user profile or change password '''
        pass

    def get(self, request, id=None):
        ''' Returns profile page with filled fields '''

        if not id: return redirect(reverse('profile', args=[request.user.id]), permanent=False)

        try:
            user = User.objects.get(id=id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        payload = {
            'id': id,
            'self_profile': request.user.id == user.id,
            'email': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'region': user.region,
            'phone': user.phone
        }

        print(payload)

        return render(request, 'profile.html', payload)
