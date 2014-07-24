from django.shortcuts import render, redirect
import commonware.log
from ffclub.person.models import Person

log = commonware.log.getLogger('ffclub')


def index(request):
    """Main view."""
    data = {}  # You'd add data here that you're sending to the template.
    return render(request, 'intro/index.html', data)


def home(request):
    """Main view."""
    data = {}  # You'd add data here that you're sending to the template.
    return render(request, 'intro/design_home.html', data)


def login_redirect(request):
    if request.user.is_authenticated() and not Person.objects.filter(user=request.user).exists():
        return redirect('user.register')
    return redirect('intro.home')
