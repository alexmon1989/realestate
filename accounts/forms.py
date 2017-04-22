from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django_select2.forms import Select2MultipleWidget, Select2Widget
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from home.models import Suburb, PricingMethod
from .models import Profile, Constants
from home.models import City


class UserForm(ModelForm):
    """Form for user data."""
    email = forms.CharField(max_length=75, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class SettingsForm(ModelForm):
    """Form for settings."""
    email = forms.CharField(max_length=75, required=True)

    class Meta:
        model = Profile
        exclude = ()


class UsersConstantsForm(ModelForm):
    """Form for user's constants."""
    class Meta:
        model = Constants
        exclude = ('user', )


class CitiesConstantsForm(forms.Form):
    """Form for city/region constants."""
    CITY_CHOICES = [(c['pk'], c['city_name']) for c in City.objects.values('pk', 'city_name').order_by('city_name')]

    city = forms.ChoiceField(label='City', widget=Select2Widget(), choices=CITY_CHOICES)
    capital_growth = forms.FloatField(
        label='Capital growth',
        min_value=0,
        help_text='Global value: <span id="global_capital_growth"></span>'
    )

    def __init__(self, *args, **kwargs):
        self.base_fields['city'].initial = kwargs.pop('active_city_id', None)

        super(CitiesConstantsForm, self).__init__(*args, **kwargs)


class HousesFilterForm(forms.Form):
    """Form for user filter settings."""
    name = forms.CharField(label='Filter Name',
                           required=False)
    suburbs = forms.MultipleChoiceField(label='Area selection',
                                        required=True)
    PRICE_FROM_CHOICES = [
        (None, 'Any'),
        (0, '$0'),
        (25000, '$25,000'),
        (50000, '$50,000'),
        (100000, '$100,000'),
        (150000, '$150,000'),
        (200000, '$200,000'),
        (250000, '$250,000'),
        (300000, '$300,000'),
        (350000, '$350,000'),
        (400000, '$400,000'),
        (450000, '$450,000'),
        (500000, '$500,000'),
        (600000, '$600,000'),
        (700000, '$700,000'),
        (800000, '$800,000'),
        (900000, '$900,000'),
        (1000000, '$1m'),
        (1200000, '$1,2m'),
        (1400000, '$1,4m'),
        (1600000, '$1,6m'),
    ]
    PRICE_TO_CHOICES = [
        (None, 'Any'),
        (0, '$0'),
        (25000, '$25,000'),
        (50000, '$50,000'),
        (100000, '$100,000'),
        (150000, '$150,000'),
        (200000, '$200,000'),
        (250000, '$250,000'),
        (300000, '$300,000'),
        (350000, '$350,000'),
        (400000, '$400,000'),
        (450000, '$450,000'),
        (500000, '$500,000'),
        (600000, '$600,000'),
        (700000, '$700,000'),
        (800000, '$800,000'),
        (900000, '$900,000'),
        (1000000, '$1m'),
        (1200000, '$1,2m'),
        (1400000, '$1,4m'),
        (2000000, '$2m'),
        (2500000, '$2,5m'),
        (3500000, '$3,5m'),
        (5000000, '$5m'),
        (7500000, '$7,5m'),
        (10000000, '$10m'),
        (999999999, '$10m+'),
    ]
    price_from = forms.ChoiceField(label='Price from',
                                   required=False,
                                   choices=PRICE_FROM_CHOICES,
                                   help_text='<a href="#" class="set-custom-value">Custom value</a>')
    price_to = forms.ChoiceField(label='Price to',
                                 required=False,
                                 choices=PRICE_TO_CHOICES,
                                 initial=999999999,
                                 help_text='<a href="#" class="set-custom-value">Custom value</a>')

    PRICING_METHODS_CHOICES = ((pricing_method.id, pricing_method.name)
                               for pricing_method in PricingMethod.objects.order_by('name'))
    pricing_methods = forms.MultipleChoiceField(label='Pricing methods',
                                                required=False,
                                                choices=PRICING_METHODS_CHOICES,
                                                widget=Select2MultipleWidget(
                                                    attrs={'data-placeholder': 'All pricing methods'}
                                                ),
                                                help_text='<a id="pricing-methods-select-all" href="#">Select all</a>')

    GOVERNMENT_VALUE_FROM_CHOICES = [
        (None, 'Any'),
        (0, '$0'),
        (25000, '$25,000'),
        (50000, '$50,000'),
        (100000, '$100,000'),
        (150000, '$150,000'),
        (200000, '$200,000'),
        (250000, '$250,000'),
        (300000, '$300,000'),
        (350000, '$350,000'),
        (400000, '$400,000'),
        (450000, '$450,000'),
        (500000, '$500,000'),
        (600000, '$600,000'),
        (700000, '$700,000'),
        (800000, '$800,000'),
        (900000, '$900,000'),
        (1000000, '$1m'),
        (1200000, '$1,2m'),
        (1400000, '$1,4m'),
        (1600000, '$1,6m'),
    ]
    GOVERNMENT_VALUE_TO_CHOICES = [
        (None, 'Any'),
        (0, '$0'),
        (25000, '$25,000'),
        (50000, '$50,000'),
        (100000, '$100,000'),
        (150000, '$150,000'),
        (200000, '$200,000'),
        (250000, '$250,000'),
        (300000, '$300,000'),
        (350000, '$350,000'),
        (400000, '$400,000'),
        (450000, '$450,000'),
        (500000, '$500,000'),
        (600000, '$600,000'),
        (700000, '$700,000'),
        (800000, '$800,000'),
        (900000, '$900,000'),
        (1000000, '$1m'),
        (1200000, '$1,2m'),
        (1400000, '$1,4m'),
        (2000000, '$2m'),
        (2500000, '$2,5m'),
        (3500000, '$3,5m'),
        (5000000, '$5m'),
        (7500000, '$7,5m'),
        (10000000, '$10m'),
        (999999999, '$10m+'),
    ]
    government_value_from = forms.ChoiceField(label='Government value from',
                                              required=False,
                                              choices=GOVERNMENT_VALUE_FROM_CHOICES,
                                              help_text='<a href="#" class="set-custom-value">Custom value</a>')
    government_value_to = forms.ChoiceField(label='Government value to',
                                            required=False,
                                            choices=GOVERNMENT_VALUE_TO_CHOICES,
                                            initial=999999999,
                                            help_text='<a href="#" class="set-custom-value">Custom value</a>')

    GOVERNMENT_VALUE_TO_PRICE_CHOICES = [
        (None, 'Any')
    ]
    for x in range(0, 21):
        t = (round(x*0.1, 1), str(round(x*0.1, 1)))
        GOVERNMENT_VALUE_TO_PRICE_CHOICES.append(t)
    GOVERNMENT_VALUE_TO_PRICE_CHOICES.append((999, '2+'))
    government_value_to_price_from = forms.ChoiceField(label='Ratio of government to price from',
                                                       required=False,
                                                       choices=GOVERNMENT_VALUE_TO_PRICE_CHOICES,
                                                       help_text='<a href="#" class="set-custom-value">Custom value</a>')

    government_value_to_price_to = forms.ChoiceField(label='Ratio of government to price to',
                                                     required=False,
                                                     choices=GOVERNMENT_VALUE_TO_PRICE_CHOICES,
                                                     initial=999,
                                                     help_text='<a href="#" class="set-custom-value">Custom value</a>')

    BEDROOMS_FROM_CHOICES = [
        (None, 'Any'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    bedrooms_from = forms.ChoiceField(label='Bedrooms from',
                                      required=False,
                                      choices=BEDROOMS_FROM_CHOICES,
                                      help_text='<a href="#" class="set-custom-value">Custom value</a>')

    BEDROOMS_TO_CHOICES = [
        (None, 'Any'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (999, '5+'),
    ]
    bedrooms_to = forms.ChoiceField(label='Bedrooms to',
                                    required=False,
                                    choices=BEDROOMS_TO_CHOICES,
                                    initial=999,
                                    help_text='<a href="#" class="set-custom-value">Custom value</a>')

    BATHROOMS_FROM_CHOICES = [
        (None, 'Any'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
    ]
    bathrooms_from = forms.ChoiceField(label='Bathrooms from',
                                       required=False,
                                       choices=BATHROOMS_FROM_CHOICES,
                                       help_text='<a href="#" class="set-custom-value">Custom value</a>')
    BATHROOMS_TO_CHOICES = [
        (None, 'Any'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (999, '3+'),
    ]
    bathrooms_to = forms.ChoiceField(label='Bathrooms to',
                                     required=False,
                                     choices=BATHROOMS_TO_CHOICES,
                                     initial=999,
                                     help_text='<a href="#" class="set-custom-value">Custom value</a>')

    LANDAREA_FROM_CHOICES = [
        (None, 'Any'),
        (0, '0 m²'),
        (100, '100 m²'),
        (200, '200 m²'),
        (300, '300 m²'),
        (500, '500 m²'),
        (750, '750 m²'),
        (1000, '1000 m²'),
        (2000, '2000 m²'),
        (5000, '5000 m²'),
        (10000, '1 HA'),
        (20000, '2 HA'),
        (50000, '5 HA'),
        (100000, '10 HA'),
        (150000, '15 HA'),
        (250000, '25 HA'),
        (999999999, '25 HA+'),
    ]
    landarea_from = forms.ChoiceField(label='Landarea from',
                                      required=False,
                                      choices=LANDAREA_FROM_CHOICES,
                                      help_text='<a href="#" class="set-custom-value">Custom value</a>')
    LANDAREA_TO_CHOICES = [
        (None, 'Any'),
        (0, '0 m²'),
        (100, '100 m²'),
        (200, '200 m²'),
        (300, '300 m²'),
        (500, '500 m²'),
        (750, '750 m²'),
        (1000, '1000 m²'),
        (2000, '2000 m²'),
        (5000, '5000 m²'),
        (10000, '1 HA'),
        (20000, '2 HA'),
        (50000, '5 HA'),
        (100000, '10 HA'),
        (150000, '15 HA'),
        (250000, '25 HA'),
        (999999999, '25 HA+'),
    ]
    landarea_to = forms.ChoiceField(label='Landarea to',
                                    required=False,
                                    choices=LANDAREA_TO_CHOICES,
                                    initial=999999999,
                                    help_text='<a href="#" class="set-custom-value">Custom value</a>')

    FLOORAREA_FROM_CHOICES = [
        (None, 'Any'),
        (0, '0 m²'),
        (20, '20 m²'),
        (40, '40 m²'),
        (60, '60 m²'),
        (80, '80 m²'),
        (100, '100 m²'),
        (120, '120 m²'),
        (150, '150 m²'),
        (180, '180 m²'),
        (999999999, '200 m²+'),
    ]
    floorarea_from = forms.ChoiceField(label='Floorarea from',
                                       required=False,
                                       choices=FLOORAREA_FROM_CHOICES,
                                       help_text='<a href="#" class="set-custom-value">Custom value</a>')

    FLOORAREA_TO_CHOICES = [
        (None, 'Any'),
        (0, '0 m²'),
        (20, '20 m²'),
        (40, '40 m²'),
        (60, '60 m²'),
        (80, '80 m²'),
        (100, '100 m²'),
        (120, '120 m²'),
        (150, '150 m²'),
        (180, '180 m²'),
        (999999999, '200 m²+'),
    ]
    floorarea_to = forms.ChoiceField(label='Floorarea to',
                                     required=False,
                                     choices=FLOORAREA_TO_CHOICES,
                                     initial=999999999,
                                     help_text='<a href="#" class="set-custom-value" >Custom value</a>')

    PROPERTY_TYPE_CHOICES = [
        ("Residential", [
            (2, 'House'),
            (1, 'Apartment'),
            (11, 'Studio'),
            (4, 'Townhouse'),
            (5, 'Unit'),
        ]),
        ("Other", [
            (8, 'Home & Income'),
            (7, 'Lifestyle Property'),
            (6, 'Lifestyle Section'),
            (12, 'Section'),
            (14, 'Retirement Living'),
            (15, 'Carpark'),
            (16, 'Boat shed'),
            (13, 'Multiple Properties'),
            (17, 'Rentals House'),
            (10, 'Rural Lifestyle Property'),
            (9, 'Rural Lifestyle Section'),
            (12, 'Section')
         ])
    ]
    property_type = forms.MultipleChoiceField(label='Property type',
                                              choices=PROPERTY_TYPE_CHOICES,
                                              required=False,
                                              widget=Select2MultipleWidget(
                                                  attrs={'data-placeholder': 'All property types'}
                                              ),
                                              help_text='<a id="property-type-select-residential" href="#">'
                                                        'Select Residential types</a><br>'
                                                        '<a id="property-type-select-other" href="#">'
                                                        'Select Other types</a><br>'
                                                        '<a id="property-type-select-all" href="#">Select all</a>')
    show_only_open_homes = forms.BooleanField(label='Show only open homes', required=False)
    show_only_properties_with_address = forms.BooleanField(label='Show only properties with an address', required=False)
    keywords = forms.CharField(label='Keywords', required=False)

    CARSPACE_FROM_CHOICES = [
        (None, 'Any'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (999, '5+'),
    ]
    carspace_from = forms.ChoiceField(label='Carspace from',
                                      required=False,
                                      choices=CARSPACE_FROM_CHOICES,
                                      help_text='<a href="#" class="set-custom-value">Custom value</a>')
    CARSPACE_TO_CHOICES = [
        (None, 'Any'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (999, '5+'),
    ]
    carspace_to = forms.ChoiceField(label='Carspace to',
                                    required=False,
                                    choices=CARSPACE_TO_CHOICES,
                                    initial=999,
                                    help_text='<a href="#" class="set-custom-value">Custom value</a>')

    ensuite = forms.BooleanField(label='Ensuite', initial=False, required=False)

    listings_age_days = forms.IntegerField(
        label='Listings age (days), not more',
        required=True,
        initial=14,
        min_value=0
    )
    
    disabled = forms.BooleanField(label='Disabled', initial=False, required=False)

    def __init__(self, *args, **kwargs):
        suburbs = [(suburb['id'], suburb['name'])
                   for suburb
                   in Suburb.objects.values('id', 'name').order_by('city__region__name', 'city__city_name', 'name')]
        self.base_fields['suburbs'].choices = suburbs

        if kwargs.get('data') or kwargs.get('initial'):
            data = kwargs.get('data') or kwargs.get('initial')

            self.check_item_exist(self.PRICE_FROM_CHOICES, data['price_from'], 'price_from')
            self.check_item_exist(self.PRICE_TO_CHOICES, data['price_to'], 'price_to')
            self.check_item_exist(self.GOVERNMENT_VALUE_FROM_CHOICES, data['government_value_from'], 'government_value_from')
            self.check_item_exist(self.GOVERNMENT_VALUE_TO_CHOICES, data['government_value_to'], 'government_value_to')
            self.check_item_exist(
                self.GOVERNMENT_VALUE_TO_PRICE_CHOICES,
                data['government_value_to_price_from'],
                'government_value_to_price_from'
            )
            self.check_item_exist(
                self.GOVERNMENT_VALUE_TO_PRICE_CHOICES,
                data['government_value_to_price_to'],
                'government_value_to_price_to'
            )
            self.check_item_exist(self.BEDROOMS_FROM_CHOICES, data['bedrooms_from'], 'bedrooms_from')
            self.check_item_exist(self.BEDROOMS_TO_CHOICES, data['bedrooms_to'], 'bedrooms_to')
            self.check_item_exist(self.BATHROOMS_FROM_CHOICES, data['bathrooms_from'], 'bathrooms_from')
            self.check_item_exist(self.BATHROOMS_TO_CHOICES, data['bathrooms_to'], 'bathrooms_to')
            self.check_item_exist(self.LANDAREA_FROM_CHOICES, data['landarea_from'], 'landarea_from')
            self.check_item_exist(self.LANDAREA_TO_CHOICES, data['landarea_to'], 'landarea_to')
            self.check_item_exist(self.FLOORAREA_FROM_CHOICES, data['floorarea_from'], 'floorarea_from')
            self.check_item_exist(self.FLOORAREA_TO_CHOICES, data['floorarea_to'], 'floorarea_to')
            self.check_item_exist(self.CARSPACE_FROM_CHOICES, data['carspace_from'], 'carspace_from')
            self.check_item_exist(self.CARSPACE_TO_CHOICES, data['carspace_to'], 'carspace_to')

        super(HousesFilterForm, self).__init__(*args, **kwargs)

    def check_item_exist(self, item_list, data, field_name):
        item_exist = False
        for x in item_list:
            if data and x[0] == float(data):
                item_exist = True
                break
        if not item_exist and data:
            item = data, data
            new_item_list = item_list.copy()
            new_item_list.extend([item])
            self.base_fields[field_name].choices = new_item_list
