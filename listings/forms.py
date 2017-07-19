import datetime
import string
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django_select2.forms import Select2MultipleWidget, Select2Widget
from .models import HouseUserData, Calculator, OtherExpense
from managers.models import Manager
from home.models import House, Region, City, Suburb


class HouseUserDataForm(ModelForm):
    rent_type = forms.ChoiceField(label='Appraisal type', choices=HouseUserData.RENT_TYPE_CHOICES, widget=forms.RadioSelect(), required=False)
    market_reg_value = forms.CharField(
        label='Market/registered value *',
    )
    managers = forms.MultipleChoiceField(label='Managers',
                                         required=False,
                                         widget=Select2MultipleWidget(
                                             attrs={'data-placeholder': 'Select managers'}
                                         ))

    def __init__(self, *args, **kwargs):
        house = kwargs.pop('house', None)
        user = kwargs.pop('user', None)
        super(HouseUserDataForm, self).__init__(*args, **kwargs)
        if house and house.price_type.pk == 1:
            help_text = '<a href="#" id="use-offer-price" class="btn btn-default btn-sm">Use Offer Price</a>&nbsp;' \
                        '<a href="#" id="use-asking-price" class="btn btn-default btn-sm">Use Asking price</a>&nbsp;' \
                        '<a href="#" id="use-government-value" class="btn btn-default btn-sm">Use Government Valuation</a>'
        else:
            help_text = '<a href="#" id="use-offer-price" class="btn btn-default btn-sm">Use Offer Price</a>&nbsp;' \
                        '<a href="#" id="use-government-value" class="btn btn-default btn-sm">Use Government Valuation</a>'

        self.fields['market_reg_value'].help_text = help_text

        managers_choices = [
            (manager.id, manager.name)
            for manager
            in Manager.objects.filter(user=user).order_by('name')
        ]
        self.fields['managers'].choices = managers_choices
        self.fields['managers'].widget.choices = managers_choices
        self.initial['managers'] = self.instance.managers.values_list('id', flat=True)

    def clean_revisit_on(self):
        revisit_on = self.cleaned_data['revisit_on']
        if revisit_on:
            present = datetime.date.today()

            if revisit_on <= present:
                raise forms.ValidationError("Field must contain future date")
        return revisit_on

    def clean_date_sold(self):
        date_sold = self.cleaned_data['date_sold']
        if date_sold:
            present = datetime.date.today()

            if date_sold > present:
                raise forms.ValidationError("Field must contain date that is earlier than or equal to today's")
        return date_sold

    class Meta:
        model = HouseUserData
        exclude = ('user', 'house')


class CalculatorForm(ModelForm):
    @staticmethod
    def get_fields_addons(users_constants, global_constants, global_capital_growth, user_capital_growth, new_build):
        if new_build:
            user_deposit = users_constants.new_built_loan_deposit
            global_deposit = global_constants.new_built_loan_deposit
        else:
            user_deposit = users_constants.loan_deposit
            global_deposit = global_constants.loan_deposit

        return {
            'property_managers_commission': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'
                                            '<a href="#" data-value="{1}" class="btn btn-warning change-value">Global value: {1}%</a>'.format(
                users_constants.property_management_commission,
                global_constants.property_management_commission,
            ),
            'int_rate': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'.format(
                users_constants.loan_interest_rate
            ),
            'deposit': '<a href="#" id="user-deposit" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'
                       '<a href="#" id="global-deposit" data-value="{1}" class="btn btn-warning change-value">Global value: {1}%</a>'.format(
                user_deposit,
                global_deposit,
            ),
            'vacancy': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}</a>'
                       '<a href="#" data-value="{1}" class="btn btn-warning change-value">Global value: {1}</a>'.format(
                users_constants.vacancy_rate,
                global_constants.vacancy_rate,
            ),
            'capital_growth': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'
                              '<a href="#" data-value="{1}" class="btn btn-warning change-value">Global value: {1}%</a>'.format(
                user_capital_growth,
                global_capital_growth or 0,
            ),
            'gross_yield': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'.format(
                users_constants.gross_yield,
            ),
            'net_yield': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: {0}%</a>'.format(
                users_constants.net_yield,
            ),
            'min_cashflow': '<a href="#" data-value="{0}" class="btn btn-primary change-value">User\'s value: $ {0}</a>'.format(
                users_constants.min_cashflow,
            ),
        }

    class Meta:
        model = Calculator
        exclude = ('user', 'house')


class OtherExpenseForm(ModelForm):
    """Form for creating OtherExpenses objects"""
    class Meta:
        model = OtherExpense
        exclude = ('user', 'house')


def file_size(value):
    """Validator for file size."""
    limit = 3 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')


class HouseForm(ModelForm):
    """Form for creating OtherExpenses objects"""
    region = forms.ModelChoiceField(label='Region', queryset=Region.objects, widget=Select2Widget())
    city = forms.ModelChoiceField(label='City', widget=Select2Widget(), queryset=City.objects)
    suburb = forms.ModelChoiceField(label='Suburb', widget=Select2Widget(), queryset=Suburb.objects)
    url = forms.CharField(required=False)
    mark = forms.ChoiceField(label='Save to list', choices=((1, 'Liked'), (2, 'Disliked')), widget=forms.RadioSelect())
    image_1 = forms.ImageField(label='Image 1', validators=[file_size], required=False)
    image_2 = forms.ImageField(label='Image 2', validators=[file_size], required=False)
    image_3 = forms.ImageField(label='Image 3', validators=[file_size], required=False)
    image_4 = forms.ImageField(label='Image 4', validators=[file_size], required=False)
    image_5 = forms.ImageField(label='Image 5', validators=[file_size], required=False)
    image_6 = forms.ImageField(label='Image 6', validators=[file_size], required=False)
    image_7 = forms.ImageField(label='Image 7', validators=[file_size], required=False)
    image_8 = forms.ImageField(label='Image 8', validators=[file_size], required=False)
    image_9 = forms.ImageField(label='Image 9', validators=[file_size], required=False)
    image_10 = forms.ImageField(label='Image 10', validators=[file_size], required=False)

    def __init__(self, *args, **kwargs):
        super(HouseForm, self).__init__(*args, **kwargs)
        try:
            suburb = self.instance.suburb
            self.fields['region'].initial = suburb.city.region
            self.fields['city'].initial = suburb.city
            self.fields['mark'].initial = self.instance.markedhouse_set.first().mark_id

            # Photos
            if self.instance.photos:
                photos = self.instance.photos.split(';')
                i = 1
                for photo in photos:
                    del self.fields['image_{}'.format(i)]
                    i += 1
        except Suburb.DoesNotExist:
            pass

    class Meta:
        model = House
        fields = (
            'region',
            'city',
            'suburb',
            'street_name',
            'street_number',
            'bedrooms',
            'bathrooms',
            'ensuite',
            'land',
            'floor',
            'car_spaces',
            'property_type',
            'price',
            'price_type',
            'auction_time',
            'description',
            'government_value',
            'government_rates',
            'url',
            'source_id',
            'additional_data',
            'property_id',
            'agency_link',
            'mark',
        )
