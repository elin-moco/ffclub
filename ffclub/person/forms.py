# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError, TextInput
from ffclub.person.models import Person


class PersonForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['fullname'].required = True
        self.fields['address'].required = True
        self.fields['occupation'].required = True

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if gender == 'unknown':
            raise ValidationError('未指定性別')
        else:
            return gender

    class Meta:
        model = Person
        fields = ('fullname', 'gender', 'address', 'occupation', 'subscribing')


class PersonEmailNicknameForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonEmailNicknameForm, self).__init__(*args, **kwargs)
        self.fields['nickname'].required = True
        self.fields['email'].required = True

    class Meta:
        model = Person
        fields = ('nickname', 'email',)
        widgets = {
            'nickname': TextInput(attrs={'placeholder': '請輸入暱稱'}),
            'email': TextInput(attrs={'placeholder': '請輸入電子郵件'}),
        }
