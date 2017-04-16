"""amsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView

from . import views

UUID_PAT = r'[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^roadmaps/$', views.roadmaps, name='roadmaps'),
    url(fr'^roadmaps/(?i)(?P<id>{UUID_PAT})/tasks/$', views.roadmap, name='roadmap'),
    url(fr'^roadmaps/(?i)(?P<roadmap>{UUID_PAT})/tasks/(?P<id>{UUID_PAT})$', views.task, name='task'),
    url(r'^$', RedirectView.as_view(url='roadmaps', permanent=False))
]
