from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages

from django_tables2 import RequestConfig

from home.models import House
from .models import MarkedHouse

from .tables import (NewListingsTable, NewListingsTableWithPhoto, LikedListingsTable, LikedListingsTableWithPhoto,
                     DislikedListingsTable, DislikedListingsTableWithPhoto, StillThinkingListingsTable,
                     StillThinkingListingsTableWithPhoto)

from decorators import group_required

from .forms import HouseUserDataForm


@login_required
@group_required('Users')
def new_listings(request):
    """Shows page with new listings."""
    # user's houses filters
    filters = request.user.housesfilter_set.filter(disabled=False).all()

    # get new houses queryset
    excluded_pks = [h.house_id for h in MarkedHouse.objects.filter(user=request.user).only('house_id')]
    houses = House.get_new_houses(filters, excluded_pks)

    # Generating table
    if request.user.profile.show_photos_filters:
        table = NewListingsTableWithPhoto(houses)
    else:
        table = NewListingsTable(houses)

    RequestConfig(request).configure(table)

    return render(request, 'listings/new.html', {
        'table': table,
        'total': len(houses)
    })


@login_required
@group_required('Users')
def liked_listings(request):
    """Shows page with liked listings."""
    houses = MarkedHouse.objects.extra(
        select={
            "address": "CONCAT_WS(' ', house.street_number, house.street_name)",
            "property_type": "CONCAT_WS(' bedrooms ', house.bedrooms, property_type.name)"
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
        'property_type'
    ).filter(user=request.user, mark_id=1)

    # Generating table
    if request.user.profile.show_photos_filters:
        table = LikedListingsTableWithPhoto(houses)
    else:
        table = LikedListingsTable(houses)
    RequestConfig(request).configure(table)

    return render(request, 'listings/liked.html', {
        'table': table,
        'total': len(houses)
    })


@login_required
@group_required('Users')
def disliked_listings(request):
    """Shows page with disliked listings."""
    houses = MarkedHouse.objects.extra(
        select={
            "address": "CONCAT_WS(' ', house.street_number, house.street_name)",
            "property_type": "CONCAT_WS(' bedrooms ', house.bedrooms, property_type.name)"
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
        'property_type'
    ).filter(user=request.user, mark_id=2)

    # Generating table
    if request.user.profile.show_photos_filters:
        table = DislikedListingsTableWithPhoto(houses)
    else:
        table = DislikedListingsTable(houses)
    RequestConfig(request).configure(table)

    return render(request, 'listings/disliked.html', {
        'table': table,
        'total': len(houses)
    })


@login_required
@group_required('Users')
def still_thinking_listings(request):
    """Shows page with still thinking listings."""
    houses = MarkedHouse.objects.extra(
        select={
            "address": "CONCAT_WS(' ', house.street_number, house.street_name)",
            "property_type": "CONCAT_WS(' bedrooms ', house.bedrooms, property_type.name)"
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
        'property_type'
    ).filter(user=request.user, mark_id=3)

    # Generating table
    if request.user.profile.show_photos_filters:
        table = StillThinkingListingsTableWithPhoto(houses)
    else:
        table = StillThinkingListingsTable(houses)
    RequestConfig(request).configure(table)

    return render(request, 'listings/still_thinking.html', {
        'table': table,
        'total': len(houses)
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
            return redirect(reverse('listings:liked_listing'))
    else:
        form = HouseUserDataForm(instance=house_user_data)

    return render(request, 'listings/show.html', {
        'house': marked_house.house,
        'photos': photos,
        'form': form,
    })


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

    return redirect(reverse('listings:show_liked_listing', args=(pk,)))


@login_required
@group_required('Users')
def mark_as_disliked(request, pk):
    """Marks house as disliked and redirects to show_disliked_listing page."""
    house = get_object_or_404(House, pk=pk)

    marked_house, created = MarkedHouse.objects.get_or_create(house=house, user=request.user)
    marked_house.mark_id = 2
    marked_house.save()
    messages.success(request, 'House has been added to "Disliked" list.')

    return redirect(reverse('listings:show_disliked_listing', args=(pk,)))


@login_required
@group_required('Users')
def mark_as_still_thinking(request, pk):
    """Marks house as disliked and redirects to show_still_thinking_listing page."""
    house = get_object_or_404(House, pk=pk)

    marked_house, created = MarkedHouse.objects.get_or_create(house=house, user=request.user)
    marked_house.mark_id = 3
    marked_house.save()
    messages.success(request, 'House has been added to "Still thinking" list.')

    return redirect(reverse('listings:show_still_thinking_listing', args=(pk,)))
