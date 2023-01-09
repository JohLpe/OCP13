from django.shortcuts import redirect, render


def homepage(request):
    """Renders website homepage"""

    return render(request, 'index.html')


def error_400(request, exception):
    """Renders bad request page"""

    return render(request, '400.html')


def error_404(request, exception):
    """Renders error 404 page"""

    return render(request, '404.html')


def error_500(request):
    """Renders server error page"""

    return render(request, '500.html')
