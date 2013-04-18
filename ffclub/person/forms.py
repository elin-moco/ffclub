# -*- coding: utf-8 -*-
from django.forms import ModelForm, ValidationError
from ffclub.person.models import Person


class PersonForm(ModelForm):

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if gender == 'unknown':
            raise ValidationError('未指定性別')
        else:
            return gender

    class Meta:
        model = Person
        fields = ('fullname', 'gender', 'address', 'occupation', 'subscribing')