from django.http import HttpResponse, JsonResponse


def bad_request(request, exception=None):
    return HttpResponse('Bad Request', status=400)


def permission_denied(request, exception=None):
    return HttpResponse('Permission Denied', status=403)


def page_not_found(request, exception=None):
    return HttpResponse('Page Not Found', status=404)


def server_error(request):
    return HttpResponse('Server Error', status=500)


