from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from decorators import group_required


@login_required
@group_required('Users')
def dashboard(request):
    """Shows dashboard page."""
    return render(request, 'home/dashboard.html')
