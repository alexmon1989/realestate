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
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.conf import settings

import json
import datetime
import os

from home.models import House, VHousesForTables, Region, City
from .models import MarkedHouse, Calculator, OtherExpense, UserHouse
from settings.models import Global as GlobalConstants
from accounts.models import CitiesConstants
from decorators import group_required

from .forms import HouseUserDataForm, CalculatorForm, OtherExpenseForm, HouseForm
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


class UsersHousesListView(ListView):
    """Shows page with houses of current user."""
    model = UserHouse

    template_name = 'listings/my.html'
    context_object_name = 'houses'

    def get_queryset(self):
        houses_list = UserHouse.objects.filter(user=self.request.user)

        # Search by keywords, address
        if self.request.GET and self.request.GET.get('keywords'):
            houses_list = houses_list.extra(
                tables=['house'],
                where=["CONCAT_WS(' ', house.street_number,	house.street_name) LIKE %s OR description = %s"],
                params=['%{}%'.format(self.request.GET['keywords']), '%{}%'.format(self.request.GET['keywords'])]
            )

        return houses_list.distinct()

    def get_context_data(self, **kwargs):
        context = super(UsersHousesListView, self).get_context_data(**kwargs)
        if self.request.GET.get('view_mode'):
            self.request.session['view_mode'] = self.request.GET['view_mode']
        elif not self.request.session.get('view_mode'):
            self.request.session['view_mode'] = 'list-view'

        context['view_mode'] = self.request.session['view_mode']
        context['total'] = len(self.object_list)

        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('per_page', 20)

    @method_decorator(login_required)
    @method_decorator(group_required(('Users', 'Self')))
    def dispatch(self, *args, **kwargs):
        return super(UsersHousesListView, self).dispatch(*args, **kwargs)


class HouseCreateView(SuccessMessageMixin, CreateView):
    """Shows page for house create"""
    template_name = 'listings/create_house.html'
    form_class = HouseForm
    success_message = 'House has been successfully created.'

    def form_valid(self, form):
        form.instance.create_time = datetime.datetime.now()
        form.instance.listing_create_date = datetime.datetime.now()
        self.object = form.save()

        user_house = UserHouse(user=self.request.user, house_id=self.object.house_id)
        user_house.save()

        marked_house = MarkedHouse(
            house_id=self.object.house_id,
            mark_id=self.request.POST.get('mark'),
            user=self.request.user
        )
        marked_house.save()

        # Images
        images_db = []
        for file in self.request.FILES:
            myfile = self.request.FILES[file]
            fs = FileSystemStorage()
            filename = fs.save(os.path.join('houses', str(self.object.house_id), myfile.name), myfile)
            uploaded_file_url = fs.url(filename)
            images_db.append(uploaded_file_url)

        self.object.photos = ';'.join(images_db)
        self.object.save()

        return super(HouseCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('listings:my_listing')

    @method_decorator(login_required)
    @method_decorator(group_required(('Users', 'Self')))
    def dispatch(self, *args, **kwargs):
        return super(HouseCreateView, self).dispatch(*args, **kwargs)


class HouseDeleteView(SuccessMessageMixin, DeleteView):
    """Deletes house."""
    template_name = 'listings/delete_house.html'
    success_message = 'House has been successfully deleted.'
    model = House

    def get_queryset(self):
        qs = super(HouseDeleteView, self).get_queryset()
        return qs.filter(userhouse__user=self.request.user)

    def get_success_url(self):
        return reverse('listings:my_listing')

    @method_decorator(login_required)
    @method_decorator(group_required(('Users', 'Self')))
    def dispatch(self, *args, **kwargs):
        return super(HouseDeleteView, self).dispatch(*args, **kwargs)


class HouseUpdateView(SuccessMessageMixin, UpdateView):
    """Shows page for update user's house."""
    template_name = 'listings/update_house.html'
    success_message = 'House data has been successfully saved.'
    form_class = HouseForm
    model = House

    def get_queryset(self):
        qs = super(HouseUpdateView, self).get_queryset()
        return qs.filter(userhouse__user=self.request.user)

    def form_valid(self, form):
        self.object = form.save()

        marked_house, created = MarkedHouse.objects.get_or_create(house=self.object, user=self.request.user)
        marked_house.mark_id = self.request.POST.get('mark')
        marked_house.save()

        # Images
        if self.object.photos:
            images_db = self.object.photos.split(';')
        else:
            images_db = []
        for file in self.request.FILES:
            myfile = self.request.FILES[file]
            fs = FileSystemStorage()
            filename = fs.save(os.path.join('houses', str(self.object.house_id), myfile.name), myfile)
            uploaded_file_url = fs.url(filename)
            images_db.append(uploaded_file_url)

        self.object.photos = ';'.join(images_db)
        self.object.save()

        return super(HouseUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('listings:my_listing')

    def get_context_data(self, **kwargs):
        context = super(HouseUpdateView, self).get_context_data(**kwargs)
        if self.object.photos:
            context['photos'] = self.object.photos.split(';')
        else:
            context['photos'] = []

        return context

    @method_decorator(login_required)
    @method_decorator(group_required(('Users', 'Self')))
    def dispatch(self, *args, **kwargs):
        return super(HouseUpdateView, self).dispatch(*args, **kwargs)


@login_required
@group_required(('Users', 'Self'))
def get_cities_by_region(request, region_id):
    region = Region.objects.get(id=region_id)
    cities = region.city_set.extra(select={'id': 'city_id', 'text': 'city_name'}).values('id', 'text').order_by('city_name')
    return JsonResponse({'results': list(cities)})


@login_required
@group_required(('Users', 'Self'))
def get_suburbs_by_city(request, city_id):
    city = City.objects.get(city_id=city_id)
    suburbs = city.suburb_set.extra(select={'id': 'id', 'text': 'name'}).values('id', 'text').order_by('name')
    return JsonResponse({'results': list(suburbs)})


@login_required
@group_required(('Users', 'Self'))
def delete_house_photo(request, house_id):
    """Deletes photo of user's house"""
    house = get_object_or_404(House, pk=house_id, userhouse__user=request.user)
    photos = house.photos.split(';')
    photos.remove(request.GET.get('photo_path'))
    house.photos = ';'.join(photos)
    house.save()

    photo_path = settings.BASE_DIR + request.GET.get('photo_path')
    if os.path.exists(photo_path):
        os.remove(photo_path)

    messages.add_message(request, messages.SUCCESS, 'Photo has been removed.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
