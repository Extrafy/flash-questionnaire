from django.http import HttpResponse

def health_check(request):
    """
    A simple view for health check.
    """
    return HttpResponse("Project is running smoothly!")