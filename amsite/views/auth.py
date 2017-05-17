from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from amsite.models import User


class LoginView(View):

    def post(self, request):
        ''' Login and register '''

        action = request.POST.get('action')

        email = request.POST.get('email')
        password = request.POST.get('password')

        if not (email and password): return JsonResponse({'ok': False, 'error': 'Empty credentials'})

        if action == 'login':
            user = authenticate(username=email, password=password)

        elif action == 'register':
            args = {}

            if request.POST.get('first_name'): args['first_name'] = request.POST.get('first_name')
            if request.POST.get('last_name'): args['last_name'] = request.POST.get('last_name')

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
    return redirect('/')
