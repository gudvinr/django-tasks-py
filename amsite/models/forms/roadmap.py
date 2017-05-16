from django.forms import ModelForm
from .. import Roadmap


class RoadmapForm(ModelForm):

    class Meta:
        model = Roadmap
        fields = ['title']
