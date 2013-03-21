from django.forms import ModelForm
from ffclub.event.models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event