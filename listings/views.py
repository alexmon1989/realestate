from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.forms.models import model_to_dict

import json

from django_tables2 import RequestConfig

from home.models import House, VHousesForTables
from .models import MarkedHouse, Calculator
from settings.models import Global as GlobalConstants
from accounts.models import CitiesConstants

from .tables import (NewListingsTable, NewListingsTableWithPhoto, LikedListingsTable, LikedListingsTableWithPhoto,
                     DislikedListingsTable, DislikedListingsTableWithPhoto, StillThinkingListingsTable,
                     StillThinkingListingsTableWithPhoto)

from decorators import group_required

from .forms import HouseUserDataForm, CalculatorForm


@login_required
@group_required('Users')
def new_listings(request):
    """Shows page with new listings."""
    # user's houses filters
    filters = request.user.housesfilter_set.filter(disabled=False).all()

    # get new houses queryset
    excluded_pks = [h.house_id for h in MarkedHouse.objects.filter(user=request.user).only('house_id')]
    houses = VHousesForTables.get_new_houses(filters, excluded_pks)

    # Generating table
    if request.user.profile.show_photos_filters:
        table = NewListingsTableWithPhoto(houses)
    else:
        table = NewListingsTable(houses)

    RequestConfig(request).configure(table)

    return render(request, 'listings/new.html', {
        'table': table,
        'total': len(table.rows)
    })


@login_required
@group_required('Users')
def liked_listings(request):
    """Shows page with liked listings."""
    houses = MarkedHouse.objects.extra(
        select={
            "address": "CASE WHEN (house.street_number <> '' AND house.street_name <> '') "
                       "THEN CONCAT_WS(' ', house.street_number, house.street_name) "
                       "ELSE 'Address not specified' END",
            "property_type": "CONCAT_WS(' bedrooms ', house.bedrooms, property_type.name)",
            "price_with_price_type": "CONCAT_WS(' ', "
                                     "CASE WHEN house.price <> 0 THEN house.price END, "
                                     "pricing_method.name)",
        }
    ).values(
        'house_id',
        'house__suburb__name',
        'house__suburb__city__city_name',
        'house__suburb__city__region__name',
        'house__street_name',
        'house__street_number',
        'house__land',
        'house__floor',
        'house__price',
        'house__listing_create_date',
        'house__photos',
        'address',
        'house__property_type__name',
        'property_type',
        'house__price_type__name',
        'price_with_price_type'
    ).filter(user=request.user, mark_id=1)

    # Generating table
    if request.user.profile.show_photos_filters:
        table = LikedListingsTableWithPhoto(houses)
    else:
        table = LikedListingsTable(houses)
    RequestConfig(request).configure(table)

    return render(request, 'listings/liked.html', {
        'table': table,
        'total': len(table.rows)
    })


@login_required
@group_required('Users')
def disliked_listings(request):
    """Shows page with disliked listings."""
    houses = MarkedHouse.objects.extra(
        select={
            "address": "CASE WHEN (house.street_number <> '' AND house.street_name <> '') "
                       "THEN CONCAT_WS(' ', house.street_number, house.street_name) "
                       "ELSE 'Address not specified' END",
            "property_type": "CONCAT_WS(' bedrooms ', house.bedrooms, property_type.name)",
            "price_with_price_type": "CONCAT_WS(' ', "
                                     "CASE WHEN house.price <> 0 THEN house.price END, "
                                     "pricing_method.name)",
        }
    ).values(
        'house_id',
        'house__suburb__name',
        'house__suburb__city__city_name',
        'house__suburb__city__region__name',
        'house__street_name',
        'house__street_number',
        'house__land',
        'house__floor',
        'house__price',
        'house__listing_create_date',
        'house__photos',
        'address',
        'house__property_type__name',
        'property_type',
        'house__price_type__name',
        'price_with_price_type'
    ).filter(user=request.user, mark_id=2)

    # Generating table
    if request.user.profile.show_photos_filters:
        table = DislikedListingsTableWithPhoto(houses)
    else:
        table = DislikedListingsTable(houses)
    RequestConfig(request).configure(table)

    return render(request, 'listings/disliked.html', {
        'table': table,
        'total': len(table.rows)
    })


@login_required
@group_required('Users')
def still_thinking_listings(request):
    """Shows page with still thinking listings."""
    houses = MarkedHouse.objects.extra(
        select={
            "address": "CASE WHEN (house.street_number <> '' AND house.street_name <> '') "
                       "THEN CONCAT_WS(' ', house.street_number, house.street_name) "
                       "ELSE 'Address not specified' END",
            "property_type": "CONCAT_WS(' bedrooms ', house.bedrooms, property_type.name)",
            "price_with_price_type": "CONCAT_WS(' ', "
                                     "CASE WHEN house.price <> 0 THEN house.price END, "
                                     "pricing_method.name)",
        }
    ).values(
        'house_id',
        'house__suburb__name',
        'house__suburb__city__city_name',
        'house__suburb__city__region__name',
        'house__street_name',
        'house__street_number',
        'house__land',
        'house__floor',
        'house__price',
        'house__listing_create_date',
        'house__photos',
        'address',
        'house__property_type__name',
        'property_type',
        'house__price_type__name',
        'price_with_price_type'
    ).filter(user=request.user, mark_id=3)

    # Generating table
    if request.user.profile.show_photos_filters:
        table = StillThinkingListingsTableWithPhoto(houses)
    else:
        table = StillThinkingListingsTable(houses)
    RequestConfig(request).configure(table)

    return render(request, 'listings/still_thinking.html', {
        'table': table,
        'total': len(table.rows)
    })


@login_required
@group_required('Users')
def show_new_listing(request, pk):
    """Shows page with house data."""
    house = get_object_or_404(House, pk=pk)
    photos = house.photos.split(';')
    return render(request, 'listings/show.html', {
        'house': house,
        'photos': photos
    })


@login_required
@group_required('Users')
def show_liked_listing(request, pk):
    """Shows page with house data."""
    # Getting house
    queryset = MarkedHouse.objects.filter(user=request.user, house_id=pk, mark_id=1)
    marked_house = get_object_or_404(queryset)
    photos = marked_house.house.photos.split(';')

    # Getting or creating house user data
    house_user_data, created = marked_house.house.houseuserdata_set.filter(
        user=request.user
    ).get_or_create(
        house=marked_house.house,
        user=request.user
    )

    # Save user data for house.
    if request.method == 'POST':
        form = HouseUserDataForm(request.POST, instance=house_user_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your data for house #{} has been saved.'.format(pk))
            return_url = reverse('listings:liked_listing')
            if request.GET.get('return_url'):
                return_url = request.GET['return_url']
            return redirect(return_url)
    else:
        form = HouseUserDataForm(instance=house_user_data)

    # Field addons
    global_constants = GlobalConstants.objects.first()
    users_constants = request.user.constants
    try:
        user_city_constants = request.user.citiesconstants_set.get(city=marked_house.house.suburb.city)
        user_capital_growth = user_city_constants.capital_growth
    except CitiesConstants.DoesNotExist:
        user_capital_growth = 0
    field_addons = CalculatorForm.get_fields_addons(
        users_constants,
        global_constants,
        marked_house.house.suburb.city.capital_growth,
        user_capital_growth
    )

    return render(request, 'listings/show.html', {
        'house': marked_house.house,
        'photos': photos,
        'form': form,
        'calculator_form': CalculatorForm(instance=Calculator.get_or_create(request.user, marked_house.house)),
        'field_addons': field_addons,
        'house_user_data': house_user_data,
        'gst': global_constants.gst
    })


@require_POST
@csrf_exempt
@login_required
@group_required('Users')
def save_calculator_data(request, house_id):
    try:
        calculator = Calculator.objects.get(user=request.user, house_id=house_id)

        calculator.managed = bool(request.POST.get('managed', True))

        if request.POST.get('property_managers_commission') != '':
            calculator.property_managers_commission = request.POST.get('property_managers_commission')
        else:
            calculator.property_managers_commission = None

        if request.POST.get('int_rate') != '':
            calculator.int_rate = request.POST.get('int_rate')
        else:
            calculator.int_rate = None

        if request.POST.get('deposit') != '':
            calculator.deposit = request.POST.get('deposit')
        else:
            calculator.deposit = None

        if request.POST.get('vacancy') != '':
            calculator.vacancy = request.POST.get('vacancy')
        else:
            calculator.vacancy = None

        if request.POST.get('capital_growth') != '':
            calculator.capital_growth = request.POST.get('capital_growth')
        else:
            calculator.capital_growth = None

        if request.POST.get('weekly_rent') != '':
            calculator.weekly_rent = request.POST.get('weekly_rent')
        else:
            calculator.weekly_rent = None

        if request.POST.get('purchase_price') != '':
            calculator.purchase_price = request.POST.get('purchase_price')
        else:
            calculator.purchase_price = None

        if request.POST.get('gross_yield') != '':
            calculator.gross_yield = request.POST.get('gross_yield')
        else:
            calculator.gross_yield = None

        if request.POST.get('net_yield') != '':
            calculator.net_yield = request.POST.get('net_yield')
        else:
            calculator.net_yield = None

        if request.POST.get('min_cashflow') != '':
            calculator.min_cashflow = request.POST.get('min_cashflow')
        else:
            calculator.min_cashflow = None

        calculator.save()
        return JsonResponse({'success': 1})
    except Calculator.DoesNotExist:
        return JsonResponse({'success': 0, 'error': 'Record not found'})


@login_required
@group_required('Users')
def reset_calculator_data(request, house_id):
    """Resets calculator data."""
    try:
        calculator = Calculator.objects.get(user=request.user, house_id=house_id)
        calculator.delete()
        calculator = Calculator.get_or_create(request.user, House.objects.get(pk=house_id))
        calculator_json = json.dumps(model_to_dict(calculator))
        return JsonResponse({'success': 1, 'calculator': calculator_json})
    except Calculator.DoesNotExist:
        return JsonResponse({'success': 0, 'error': 'Record not found'})


@login_required
@group_required('Users')
def show_disliked_listing(request, pk):
    """Shows page with house data."""
    house = get_object_or_404(House, pk=pk)
    photos = house.photos.split(';')
    return render(request, 'listings/show.html', {
        'house': house,
        'photos': photos
    })


@login_required
@group_required('Users')
def show_still_thinking_listing(request, pk):
    """Shows page with house data."""
    house = get_object_or_404(House, pk=pk)
    photos = house.photos.split(';')
    return render(request, 'listings/show.html', {
        'house': house,
        'photos': photos
    })


@login_required
@group_required('Users')
def mark_as_liked(request, pk):
    """Marks house as liked and redirects to show_liked_listing page."""
    house = get_object_or_404(House, pk=pk)
    marked_house, created = MarkedHouse.objects.get_or_create(house=house, user=request.user)
    marked_house.mark_id = 1
    marked_house.save()
    messages.success(request, 'House has been added to "Liked" list.')

    return_url = reverse('listings:new_listing')
    if request.GET.get('return_url'):
        return_url = request.GET['return_url']

    return redirect('{}?return_url={}'.format(
        reverse('listings:show_liked_listing', args=(pk,)),
        return_url
    ))


@login_required
@group_required('Users')
def mark_as_disliked(request, pk):
    """Marks house as disliked and redirects to show_disliked_listing page."""
    house = get_object_or_404(House, pk=pk)

    marked_house, created = MarkedHouse.objects.get_or_create(house=house, user=request.user)
    marked_house.mark_id = 2
    marked_house.save()
    messages.success(request, 'House has been added to "Disliked" list.')

    return_url = reverse('listings:new_listing')
    if request.GET.get('return_url'):
        return_url = request.GET['return_url']

    return redirect(return_url)


@login_required
@group_required('Users')
def mark_as_still_thinking(request, pk):
    """Marks house as disliked and redirects to show_still_thinking_listing page."""
    house = get_object_or_404(House, pk=pk)

    marked_house, created = MarkedHouse.objects.get_or_create(house=house, user=request.user)
    marked_house.mark_id = 3
    marked_house.save()
    messages.success(request, 'House has been added to "Still thinking" list.')

    return_url = reverse('listings:new_listing')
    if request.GET.get('return_url'):
        return_url = request.GET['return_url']

    return redirect(return_url)
