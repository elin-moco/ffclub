from django.http import HttpResponse


ACC_HEADERS = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
               'Access-Control-Max-Age': 1000,
               'Access-Control-Allow-Headers': '*'}


def cors_allow(func):
    """ Sets Access Control request headers."""

    def wrap(request, *args, **kwargs):
        # Firefox sends 'OPTIONS' request for cross-domain javascript call.
        if request.method != "OPTIONS":
            response = func(request, *args, **kwargs)
        else:
            response = HttpResponse()
        for k, v in ACC_HEADERS.iteritems():
            response[k] = v
        return response

    return wrap


def enable_jsonp(func):
    def wrap(request, *args, **kwargs):
        callback = request.GET.get('callback')
        if callback:
            try:
                response = func(request, *args, **kwargs)
            except Exception as e:
                print e
                response = HttpResponse('error', status=500)
            if response.status_code / 100 != 2:
                response.content = 'error'
            if response.content[0] not in ['"', '[', '{'] \
                    or response.content[-1] not in ['"', ']', '}']:
                response.content = '"%s"' % response.content
            response.content = "%s(%s)" % (callback, response.content)
            response['Content-Type'] = 'application/javascript'
        else:
            response = func(request, *args, **kwargs)
        return response

    return wrap
