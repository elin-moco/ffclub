from django.core.exceptions import PermissionDenied
from django.shortcuts import *
from django.contrib import auth
import commonware

from forms import PersonForm
from models import Person


log = commonware.log.getLogger('ffclub')


def register(request):
    """Main view."""
    if not request.user.is_authenticated():
        raise PermissionDenied
    if request.method == 'POST':
        is_update = Person.objects.filter(user=request.user).exists()
        if is_update:
            form = PersonForm(request.POST, instance=Person.objects.get(user=request.user))
        else:
            form = PersonForm(request.POST)
        data = {'form': form}
        if form.is_valid():
            person = form.save(commit=False)
            if is_update:
                person.save()
                return redirect('intro.home')
            else:
                person.user = auth.get_user(request)
                person.save()
                return redirect('user.register.complete')
    elif Person.objects.filter(user=request.user).exists():
        data = {'form': PersonForm(instance=request.user.get_profile())}
    else:
        data = {'form': PersonForm()}  # You'd add data here that you're sending to the template.

    return render(request, 'person/register.html', data)


def register_complete(request):
    """Main view."""
    data = {}  # You'd add data here that you're sending to the template.

    return render(request, 'person/register_complete.html', data)
