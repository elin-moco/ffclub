from django.forms import ModelForm
from ffclub.person.models import Person


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('fullname', 'gender', 'address', 'occupation')