from django.conf import settings


def portal_settings(request):
    return {
        'pcshop_url': settings.PCSHOP_URL,
    }
