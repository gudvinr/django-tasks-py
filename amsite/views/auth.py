from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from ..models import User, forms


def append_to_dict(form, args, field):
    if form.cleaned_data[field]: args[field] = form.cleaned_data[field]


class LoginView(View):

    def post(self, request):
        ''' Login and register '''

        form = forms.UserForm(request.POST)
        if not form.is_valid(): return JsonResponse({'ok': False, 'error': str(form.errors)})

        action = form.cleaned_data['action']

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        if not (email and password): return JsonResponse({'ok': False, 'error': 'Empty credentials'})

        if action == 'login':
            user = authenticate(username=email, password=password)

        elif action == 'register':
            args = {}

            append_to_dict(form, args, 'first_name')
            append_to_dict(form, args, 'last_name')
            append_to_dict(form, args, 'age')
            append_to_dict(form, args, 'region')
            append_to_dict(form, args, 'phone')

            user = User.objects.create_user(username=email, password=password, **args)
        else:
            return JsonResponse({'ok': False, 'error': 'Wrong action'})

        if not user: return JsonResponse({'ok': False, 'error': 'Wrong credentials'})

        login(request, user)

        return JsonResponse({'ok': True, 'result': reverse('roadmaps')})

    def get(self, request):
        ''' Render auth view '''

        return render(request, 'auth.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/', permanent=False)
