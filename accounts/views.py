from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm

from decorators import group_required

from .forms import UserForm


@login_required
@group_required('Users')
def profile(request):
    return render(request, 'accounts/profile.html', {
        'form_user_data': UserForm(instance=request.user),
        'form_change_password': PasswordChangeForm(request.user),
    })


@require_POST
@login_required
@group_required('Users')
def save_user_data(request):
    form = UserForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'User data successfully saved.')
        return redirect('{}?active_tab=user-data'.format(reverse('accounts:profile')))
    return render(request, 'accounts/profile.html', {
        'form_user_data': form,
        'form_change_password': PasswordChangeForm(request.user)
    })


@require_POST
@login_required
@group_required('Users')
def save_search_data(request):
    pass


@require_POST
@login_required
@group_required('Users')
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Your password was successfully updated!')
        return redirect('{}?active_tab=change-password'.format(reverse('accounts:profile')))
    return render(request, 'accounts/profile.html', {
        'form_user_data': UserForm(instance=request.user),
        'form_change_password': form
    })
