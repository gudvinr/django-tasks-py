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
    url(r'^roadmaps/?$', views.RoadmapsView.as_view(), name='roadmaps'),

    url(r'^roadmaps/(?i)(?P<id>{})/tasks/?$'.format(UUID_PAT), views.RoadmapView.as_view(), name='roadmap'),
    url(r'^roadmaps/(?i)(?P<id>{})/stat/?$'.format(UUID_PAT), views.RoadmapStatView.as_view(), name='rm_stat'),

    url(r'^roadmaps/(?i)(?P<roadmap>{0})/tasks/(?P<id>{0})$'.format(UUID_PAT), views.TaskView.as_view(), name='task'),

    url(r'^profile/(?i)(?P<id>{})/?'.format(UUID_PAT), views.ProfileView.as_view(), name='profile'),
    url(r'^profile/?', views.ProfileView.as_view(), name='profile'),
    url(r'^auth/?', views.LoginView.as_view(), name='auth'),
    url(r'^logout/?', views.logout_view, name='logout'),

    url(r'^admin/?', admin.site.urls),

    url(r'^.*$', RedirectView.as_view(url='/roadmaps', permanent=False))
]
