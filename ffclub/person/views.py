from django.shortcuts import *
from .forms import PersonForm
from django.contrib import auth

import commonware

log = commonware.log.getLogger('ffclub')


def register(request):
    """Main view."""
    if request.method == 'POST':
        form = PersonForm(request.POST)
        data = {'form': form}
        if form.is_valid():
            person = form.save(commit=False)
            person.user = auth.get_user(request)
            person.save()
            return redirect('user.register.complete')
    else:
        data = {'form': PersonForm()}  # You'd add data here that you're sending to the template.

    return render(request, 'person/register.html', data)


def register_complete(request):
    """Main view."""
    data = {}  # You'd add data here that you're sending to the template.

    return render(request, 'person/register_complete.html', data)
