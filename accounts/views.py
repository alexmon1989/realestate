from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from decorators import group_required


@login_required
@group_required('Users')
def profile(request):
    return HttpResponse("Profile page.")
