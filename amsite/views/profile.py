from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse

from ..models import User, forms


class ProfileView(LoginRequiredMixin, View):

    def post(self, request, id=None):
        ''' Edit user profile or change password '''

        if not id: return JsonResponse({'ok': False, 'error': "No such user: {}".format(id)})

        try:
            user = User.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({'ok': False, 'error': "Can't find user: {}".format(id)})

        form = forms.UserForm(request.POST, instance=user)
        if not form.is_valid(): return JsonResponse({'ok': False, 'error': str(form.errors)})

        if form.cleaned_data['email'] and form.cleaned_data['email'] != user.username:
            return JsonResponse({'ok': False, 'error': "Email can't be changed"})

        if form.cleaned_data['password'] and form.cleaned_data['password'] != form.cleaned_data['password_confirm']:
            return JsonResponse({'ok': False, 'error': "Passwords does not match"})

        user = form.save(commit=False)

        if form.cleaned_data['password']: user.set_password(form.cleaned_data['password'])
        user.save()

        return JsonResponse({'ok': True})

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
