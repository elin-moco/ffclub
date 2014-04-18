from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ffclub.newsletter.models import Subscription
from ffclub.settings import API_SECRET
from .utils import *
from django.core import serializers
import json


def subscription_count(request):
    if 'secret' in request.GET and request.GET['secret'] == API_SECRET:
        count = Subscription.objects.filter(status=1).exclude(email__isnull=True).exclude(email__exact='').count()
    else:
        raise PermissionDenied
    return HttpResponse(str(count), content_type='application/json')


def subscribed(request):
    if 'secret' in request.GET and request.GET['secret'] == API_SECRET and 'email' in request.GET:
        exists = Subscription.objects.filter(status=1, email=request.GET['email']).exists()
    else:
        raise PermissionDenied
    return HttpResponse(str(exists), content_type='application/json')


@csrf_exempt
def subscribe(request):
    if request.method == 'POST' and 'secret' in request.POST and request.POST['secret'] == API_SECRET and 'email' in request.POST:
        result = newsletter_subscribe(request.POST['email'])
    else:
        raise PermissionDenied
    return HttpResponse(str('True'), content_type='application/json')


@csrf_exempt
def unsubscribe(request):
    if request.method == 'POST' and 'secret' in request.POST and request.POST['secret'] == API_SECRET and 'email' in request.POST:
        result = newsletter_unsubscribe(request.POST['email'])
    else:
        raise PermissionDenied
    return HttpResponse(str(result), content_type='application/json')


def newsletter(request, page_number='1'):
    context = {}
    ITEMS_PER_PAGE = 10
    if request.method == 'GET' and 'secret' in request.GET and request.GET['secret'] == API_SECRET:
        query = Newsletter.objects.filter(publish_date__lte=datetime.now()).order_by('-issue')
        result = list(Paginator(query, ITEMS_PER_PAGE).page(page_number))
        meta = list(MetaFile.objects.filter(name='main-thumb', issue__in=result))
        response = []
        for newsletter in result:
            issue_format = '%Y-%m-%d' if newsletter.volume > 16 else '%Y-%m'
            thumb = next((os.path.basename(x.value.name) for x in meta if x.issue == newsletter), None)
            response += [{
                'volume': newsletter.volume,
                'issue': newsletter.issue.strftime(issue_format),
                'title': newsletter.title,
                'main-thumb': thumb,
            }, ]
            context = {'total': query.count(), 'count': ITEMS_PER_PAGE, 'page': int(page_number), 'newsletters': response}
    else:
        raise PermissionDenied
    return HttpResponse(json.dumps(context), content_type='application/json')
