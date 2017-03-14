from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic.edit import DeleteView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.http import JsonResponse

import json

from decorators import group_required

from .forms import UserForm, HousesFilterForm

from .models import HousesFilter
from home.models import Suburb, PropertyType

from .tables import FiltersTable


@login_required
@group_required('Users')
def profile(request):
    """Shows profile data in forms for edit."""
    filters_data = []
    filters = request.user.housesfilter_set.all()
    for f in filters:
        filter_data_json = json.loads(f.filter_data_json)
        filters_data.append({
            'id': f.id,
            'name': f.name,
            'suburbs': ', '.join([suburb.name for suburb in Suburb.objects.filter(pk__in=filter_data_json['suburbs'])]),
            'price_from': filter_data_json['price_from'][0],
            'price_to': filter_data_json['price_to'][0],
            'landarea_from': filter_data_json['landarea_from'][0],
            'landarea_to': filter_data_json['landarea_to'][0],
            'property_type': ', '.join([property_type.name
                                        for property_type
                                        in PropertyType.objects.filter(pk__in=filter_data_json['property_type'])]),
            'disabled': f.disabled,
            'created_at': f.created_at,
            'updated_at': f.updated_at,
            'actions': f.id,
        })

    filters_table = FiltersTable(filters_data)
    return render(request, 'accounts/profile.html', {
        'form_user_data': UserForm(instance=request.user),
        'form_change_password': PasswordChangeForm(request.user),
        'form_user_filter_settings': HousesFilterForm(),
        'filters_table': filters_table
    })


@login_required
@group_required('Users')
def create_filter(request):
    """Creates user filter."""
    if request.method == 'POST':
        form = HousesFilterForm(request.POST)
        if form.is_valid():
            new_filter = HousesFilter(filter_data_json=json.dumps(dict(request.POST)), user_id=request.user.pk)
            new_filter.disabled = bool(request.POST.get('disabled', False))
            new_filter.name = request.POST.get('name')
            new_filter.save()
            messages.success(request, 'The new filter has been successfully created.')
            return redirect('{}?active_tab=filters'.format(reverse('accounts:profile')))
    else:
        form = HousesFilterForm()

    return render(request, 'accounts/create_filter.html', {'form': form})


@login_required
@group_required('Users')
def edit_filter(request, pk):
    """Edits user filter."""
    house_filter = get_object_or_404(HousesFilter.objects.filter(user=request.user), pk=pk)
    if request.method == 'POST':
        form = HousesFilterForm(request.POST)
        if form.is_valid():
            house_filter.filter_data_json = json.dumps(dict(request.POST))
            house_filter.disabled = bool(request.POST.get('disabled', False))
            house_filter.name = request.POST.get('name')
            house_filter.save()
            messages.success(request, 'The filter has been successfully updated.')
            return redirect(reverse('accounts:edit_filter', args=(pk,)))
    else:
        filter_data_json = json.loads(house_filter.filter_data_json)
        house_filter_dict = {}
        for key, value in filter_data_json.items():
            if len(value) == 1:
                house_filter_dict[key] = value[0]
            else:
                house_filter_dict[key] = value
        form = HousesFilterForm(initial=house_filter_dict)

    return render(request, 'accounts/edit_filter.html', {'form': form})


class FilterDeleteView(SuccessMessageMixin, DeleteView):
    """Deletes user filter."""
    model = HousesFilter
    success_message = "The filter has been successfully deleted."

    def get_success_url(self):
        """URL for success redirect."""
        return '{}?active_tab=filters'.format(reverse('accounts:profile'))

    def get_queryset(self):
        """User can delete only own filters."""
        qs = super(FilterDeleteView, self).get_queryset()
        return qs.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(FilterDeleteView, self).delete(request, *args, **kwargs)

    @method_decorator(login_required)
    @method_decorator(group_required('Users'))
    def dispatch(self, *args, **kwargs):
        return super(FilterDeleteView, self).dispatch(*args, **kwargs)


@require_POST
@login_required
@group_required('Users')
def save_user_data(request):
    """Changes user's data."""
    form = UserForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'User data successfully saved.')
        return redirect('{}?active_tab=user-data'.format(reverse('accounts:profile')))
    return render(request, 'accounts/profile.html', {
        'form_user_data': form,
        'form_change_password': PasswordChangeForm(request.user),
        'form_user_filter_settings': HousesFilterForm(request.user),
    })


@require_POST
@login_required
@group_required('Users')
def change_password(request):
    """Changes user's password."""
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Your password was successfully updated!')
        return redirect('{}?active_tab=change-password'.format(reverse('accounts:profile')))
    return render(request, 'accounts/profile.html', {
        'form_user_data': UserForm(instance=request.user),
        'form_change_password': form,
        'form_user_filter_settings': HousesFilterForm(request.user),
    })


@require_POST
@login_required
@group_required('Users')
@csrf_exempt
def change_show_title_photo(request):
    """Changes show_title_photo field of Profile model."""
    request.user.profile.show_photos_filters = request.POST.get('value', False)
    request.user.save()

    return JsonResponse({'success': True})


@require_POST
@login_required
@group_required('Users')
@csrf_exempt
def change_font_size(request):
    """Changes font size ration in profile data."""
    current_ratio = request.user.profile.font_ratio
    if request.POST.get('action') == 'increase':
        current_ratio += 0.1
    else:
        current_ratio -= 0.1

    request.user.profile.font_ratio = current_ratio
    request.user.profile.save()

    return JsonResponse({'success': True, 'ratio': round(current_ratio, 1)})
