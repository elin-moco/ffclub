from django.forms import ModelForm
from ffclub.event.models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'location', 'num_of_ppl')
