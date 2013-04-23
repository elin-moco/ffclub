# -*- coding: utf-8 -*-
from django.shortcuts import render


def csrf_failure(request, reason=''):
    data = {'reason': reason}
    return render(request, '403.html', data)
