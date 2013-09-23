from ffclub import settings


def constants(request):
    """
    Adds media-related context variables to the context.

    """
    return {
        'FB_APP_ID': settings.FB_APP_ID,
        'FB_APP_NAMESPACE': settings.FB_APP_NAMESPACE,
        'DEBUG': settings.DEBUG,
    }
