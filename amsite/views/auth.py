from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse


class LoginView(View):

    def post(self, request):
        ''' Login and register '''

        email = request.POST.get('email')
        password = request.POST.get('password')

        if not (email and password): return JsonResponse({'ok': False, 'error': 'Empty credentials'})

        user = authenticate(username=email, password=password)

        if not user: return JsonResponse({'ok': False, 'error': 'Wrong credentials'})

        login(request, user)

        return JsonResponse({'ok': True, 'result': reverse('roadmaps')})

    def get(self, request):
        ''' Render auth view '''

        return render(request, 'auth.html')


@login_required
def logout_view(request):
    if request.method == 'POST': logout(request)

    return redirect('/')
