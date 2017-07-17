from django.shortcuts import render, redirect, reverse
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from django.db.models import Sum, Q

import json
import datetime

from django_tables2 import RequestConfig

from home.models import House, VHousesForTables, RentalAnalysis, SalesPrices
from .models import MarkedHouse, Calculator, OtherExpense
from settings.models import Global as GlobalConstants
from accounts.models import CitiesConstants

from .tables import (NewListingsTable, NewListingsTableWithPhoto, LikedListingsTable, LikedListingsTableWithPhoto,
                     DislikedListingsTable, DislikedListingsTableWithPhoto, StillThinkingListingsTable,
                     StillThinkingListingsTableWithPhoto)

from decorators import group_required

from .forms import HouseUserDataForm, CalculatorForm, OtherExpenseForm
from managers.forms import ManagerForm


@login_required
@group_required(('Users', 'Self'))
def new_listings(request):
    """Shows page with new listings."""
    # user's houses filters
    filters = request.user.housesfilter_set.filter(disabled=False).all()

    # get new houses queryset
    excluded_pks = [h.house_id for h in MarkedHouse.objects.filter(user=request.user).only('house_id')]
    houses_list = VHousesForTables.get_new_houses(filters, excluded_pks)

    # Search by keywords, address
    if request.GET and request.GET.get('keywords'):
        houses_list = houses_list.filter(Q(description__contains=request.GET['keywords'])
                               | Q(address__contains=request.GET['keywords']))

    # Pagination
    paginator = Paginator(houses_list, request.GET.get('per_page', 20))
    page = request.GET.get('page')
    try:
        houses = paginator.page(page)
    except PageNotAnInteger:
        houses = paginator.page(1)
    except EmptyPage:
        houses = paginator.page(paginator.num_pages)

    if request.GET.get('view_mode'):
        request.session['view_mode'] = request.GET['view_mode']
    elif not request.session.get('view_mode'):
        request.session['view_mode'] = 'list-view'

    return render(request, 'listings/new.html', {
        'houses': houses,
        'total': len(houses_list),
        'pages': range(1, paginator.num_pages + 1),
        'view_mode': request.session['view_mode'],
    })


@login_required
@group_required(('Users', 'Self'))
def liked_listings(request):
    """Shows page with liked listings."""
    houses_list = MarkedHouse.objects.extra(
        select={
            "address": "CASE WHEN (house.street_number <> '' AND house.street_name <> '') "
                       "THEN CONCAT_WS(' ', house.street_number, house.street_name) "
                       "ELSE 'Address not specified' END",
            "property_type": "CONCAT_WS(' bedrooms ', house.bedrooms, property_type.name)",
            "price_with_price_type": "CASE "
                                     "WHEN (`house`.`price` <> 0) "
                                     "THEN FORMAT(`house`.`price`, 0) "
                                     "ELSE `pricing_method`.`name` "
                                     "END"
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
        'house__bedrooms',
        'house__bathrooms',
        'house__description',
        'address',
        'house__property_type__name',
        'property_type',
        'house__price_type__name',
        'price_with_price_type'
    ).filter(user=request.user, mark_id=1)

    # Search by keywords, address
    if request.GET and request.GET.get('keywords'):
        houses_list = houses_list.extra(
            where=["CONCAT_WS(' ', house.street_number,	house.street_name) LIKE %s OR description = %s"],
            params=['%{}%'.format(request.GET['keywords']), '%{}%'.format(request.GET['keywords'])]
        )

    # Pagination
    paginator = Paginator(houses_list, request.GET.get('per_page', 20))
    page = request.GET.get('page')
    try:
        houses = paginator.page(page)
    except PageNotAnInteger:
        houses = paginator.page(1)
    except EmptyPage:
        houses = paginator.page(paginator.num_pages)

    if request.GET.get('view_mode'):
        request.session['view_mode'] = request.GET['view_mode']
    elif not request.session.get('view_mode'):
        request.session['view_mode'] = 'list-view'

    if request.GET.get('view_mode'):
        request.session['view_mode'] = request.GET['view_mode']
    elif not request.session.get('view_mode'):
        request.session['view_mode'] = 'list-view'

    return render(request, 'listings/liked.html', {
        'houses': houses,
        'total': len(houses_list),
        'pages': range(1, paginator.num_pages + 1),
        'view_mode': request.session['view_mode'],
    })


@login_required
@group_required(('Users', 'Self'))
def disliked_listings(request):
    """Shows page with disliked listings."""
    houses_list = MarkedHouse.objects.extra(
        select={
            "address": "CASE WHEN (house.street_number <> '' AND house.street_name <> '') "
                       "THEN CONCAT_WS(' ', house.street_number, house.street_name) "
                       "ELSE 'Address not specified' END",
            "property_type": "CONCAT_WS(' bedrooms ', house.bedrooms, property_type.name)",
            "price_with_price_type": "CASE "
                                     "WHEN (`house`.`price` <> 0) "
                                     "THEN FORMAT(`house`.`price`, 0) "
                                     "ELSE `pricing_method`.`name` "
                                     "END"
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
        'house__bedrooms',
        'house__bathrooms',
        'house__description',
        'address',
        'house__property_type__name',
        'property_type',
        'house__price_type__name',
        'price_with_price_type'
    ).filter(user=request.user, mark_id=2)

    # Search by keywords, address
    if request.GET and request.GET.get('keywords'):
        houses_list = houses_list.extra(
            where=["CONCAT_WS(' ', house.street_number,	house.street_name) LIKE %s OR description = %s"],
            params=['%{}%'.format(request.GET['keywords']), '%{}%'.format(request.GET['keywords'])]
        )

    # Pagination
    paginator = Paginator(houses_list, request.GET.get('per_page', 20))
    page = request.GET.get('page')
    try:
        houses = paginator.page(page)
    except PageNotAnInteger:
        houses = paginator.page(1)
    except EmptyPage:
        houses = paginator.page(paginator.num_pages)

    if request.GET.get('view_mode'):
        request.session['view_mode'] = request.GET['view_mode']
    elif not request.session.get('view_mode'):
        request.session['view_mode'] = 'list-view'

    if request.GET.get('view_mode'):
        request.session['view_mode'] = request.GET['view_mode']
    elif not request.session.get('view_mode'):
        request.session['view_mode'] = 'list-view'

    return render(request, 'listings/disliked.html', {
        'houses': houses,
        'total': len(houses_list),
        'pages': range(1, paginator.num_pages + 1),
        'view_mode': request.session['view_mode'],
    })


@login_required
@group_required(('Users', 'Self'))
def still_thinking_listings(request):
    """Shows page with still thinking listings."""
    houses_list = MarkedHouse.objects.extra(
        select={
            "address": "CASE WHEN (house.street_number <> '' AND house.street_name <> '') "
                       "THEN CONCAT_WS(' ', house.street_number, house.street_name) "
                       "ELSE 'Address not specified' END",
            "property_type": "CONCAT_WS(' bedrooms ', house.bedrooms, property_type.name)",
            "price_with_price_type": "CASE "
                                     "WHEN (`house`.`price` <> 0) "
                                     "THEN FORMAT(`house`.`price`, 0) "
                                     "ELSE `pricing_method`.`name` "
                                     "END"
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
        'house__bedrooms',
        'house__bathrooms',
        'house__description',
        'address',
        'house__property_type__name',
        'property_type',
        'house__price_type__name',
        'price_with_price_type'
    ).filter(user=request.user, mark_id=3)

    # Search by keywords, address
    if request.GET and request.GET.get('keywords'):
        houses_list = houses_list.extra(
            where=["CONCAT_WS(' ', house.street_number,	house.street_name) LIKE %s OR description = %s"],
            params=['%{}%'.format(request.GET['keywords']), '%{}%'.format(request.GET['keywords'])]
        )

    # Search by keywords, address
    if request.GET and request.GET.get('keywords'):
        houses_list = houses_list.extra(
            where=["CONCAT_WS(' ', house.street_number,	house.street_name) LIKE %s OR description = %s"],
            params=['%{}%'.format(request.GET['keywords']), '%{}%'.format(request.GET['keywords'])]
        )

    # Pagination
    paginator = Paginator(houses_list, request.GET.get('per_page', 20))
    page = request.GET.get('page')
    try:
        houses = paginator.page(page)
    except PageNotAnInteger:
        houses = paginator.page(1)
    except EmptyPage:
        houses = paginator.page(paginator.num_pages)

    if request.GET.get('view_mode'):
        request.session['view_mode'] = request.GET['view_mode']
    elif not request.session.get('view_mode'):
        request.session['view_mode'] = 'list-view'

    if request.GET.get('view_mode'):
        request.session['view_mode'] = request.GET['view_mode']
    elif not request.session.get('view_mode'):
        request.session['view_mode'] = 'list-view'

    return render(request, 'listings/still_thinking.html', {
        'houses': houses,
        'total': len(houses_list),
        'pages': range(1, paginator.num_pages + 1),
        'view_mode': request.session['view_mode'],
    })


@login_required
@group_required(('Users', 'Self'))
def show_new_listing(request, pk):
    """Shows page with house data."""
    house = get_object_or_404(House, pk=pk)
    photos = house.photos.split(';')
    return render(request, 'listings/show.html', {
        'house': house,
        'photos': photos
    })


@login_required
@group_required(('Users', 'Self'))
def show_liked_listing(request, pk):
    """Shows page with house data."""
    if request.method == 'GET':
        return_url = request.GET.get('return_url')
        if return_url and return_url != 'search':
            resolve(return_url)

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
        form = HouseUserDataForm(request.POST, instance=house_user_data, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your data for house #{} has been saved.'.format(pk))
            return_url = reverse('listings:liked_listing')
            if request.GET.get('return_url'):
                return_url = request.GET['return_url']
            if request.POST.get('return_url'):
                return_url = request.POST['return_url']
            return redirect(return_url)
    else:
        form = HouseUserDataForm(instance=house_user_data, house=marked_house.house, user=request.user)

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
        user_capital_growth,
        house_user_data.new_build
    )

    # Statistical data
    rental_analysis = marked_house.house.suburb.rentalanalysis_set.filter(
        property_type_id=marked_house.house.property_type_id,
        bedrooms=marked_house.house.bedrooms
    ).first()
    sales_prices = marked_house.house.suburb.salesprices_set.filter(
        property_type_id=marked_house.house.property_type_id
    ).first()

    manager_form = ManagerForm()

    return render(request, 'listings/show.html', {
        'house': marked_house.house,
        'photos': photos,
        'form': form,
        'calculator_form': CalculatorForm(instance=Calculator.get_or_create(request.user, marked_house.house)),
        'field_addons': field_addons,
        'house_user_data': house_user_data,
        'gst': global_constants.gst,
        'total_other_expenses': house_user_data.otherexpense_set.aggregate(Sum('value'))['value__sum'] or 0,
        'form_create_expense': OtherExpenseForm(),
        'open_homes': marked_house.house.openhomes_set.filter(date_from__gte=datetime.date.today()).order_by('date_from').values(
            'date_from',
            'date_to'
        ),
        'rental_analysis': rental_analysis,
        'sales_prices': sales_prices,
        'manager_form': manager_form,
    })


@login_required
@group_required(('Users', 'Self'))
def delete_other_expenses_item(request, pk):
    """Deletes other expense item."""
    try:
        expense = OtherExpense.objects.get(pk=pk)
    except OtherExpense.DoesNotExist:
        return JsonResponse({'success': 0, 'error': 'Item not found.'}, status=404)

    # Check if it is expense item of this user
    if expense.house_user_data.user.pk != request.user.pk:
        return JsonResponse({'success': 0, 'error': 'Item not found.'}, status=404)

    expense.delete()

    return JsonResponse({
        'success': 1,
        'total_other_expenses': OtherExpense.objects.filter(
            house_user_data__user=request.user,
            house_user_data__house=expense.house_user_data.house
        ).aggregate(Sum('value'))
    })


@require_POST
@csrf_exempt
@login_required
@group_required(('Users', 'Self'))
def create_other_expenses_item(request):
    """Deletes other expense item."""
    form = OtherExpenseForm(request.POST)
    if form.is_valid():
        expense = form.save()

        return JsonResponse({
            'success': 1,
            'pk': expense.pk,
            'key': expense.key,
            'value': expense.value,
            'total_other_expenses': OtherExpense.objects.filter(
                house_user_data__user=request.user,
                house_user_data__house=expense.house_user_data.house
            ).aggregate(Sum('value'))
        })
    else:
        return JsonResponse({'success': 0, 'errors': form.errors}, status=422)


@require_POST
@csrf_exempt
@login_required
@group_required(('Users', 'Self'))
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
@group_required(('Users', 'Self'))
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
@group_required(('Users', 'Self'))
def show_disliked_listing(request, pk):
    """Shows page with house data."""
    house = get_object_or_404(House, pk=pk)
    photos = house.photos.split(';')
    return render(request, 'listings/show.html', {
        'house': house,
        'photos': photos
    })


@login_required
@group_required(('Users', 'Self'))
def show_still_thinking_listing(request, pk):
    """Shows page with house data."""
    house = get_object_or_404(House, pk=pk)
    photos = house.photos.split(';')
    return render(request, 'listings/show.html', {
        'house': house,
        'photos': photos
    })


@login_required
@group_required(('Users', 'Self'))
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
@group_required(('Users', 'Self'))
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
        if return_url == 'search':
            return_url = request.session['search_uri']

    return redirect(return_url)


@login_required
@group_required(('Users', 'Self'))
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
        if return_url == 'search':
            return_url = request.session['search_uri']

    return redirect(return_url)


@login_required
@group_required(('Users', 'Self'))
def get_deposit_values(request):
    """Returns JSON with current deposit values."""
    global_constants = GlobalConstants.objects.first()
    users_constants = request.user.constants

    if int(request.GET.get('is_new_build')) == 1:
        res = {
            'global_deposit': global_constants.new_built_loan_deposit,
            'user_deposit': users_constants.new_built_loan_deposit,
        }
    else:
        res = {
            'global_deposit': global_constants.loan_deposit,
            'user_deposit': users_constants.loan_deposit,
        }

    return JsonResponse(res)
