from django.shortcuts import render


def dashboard(request):
    """Shows dashboard page."""
    return render(request, 'home/dashboard.html')
