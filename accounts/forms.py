from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django_select2.forms import Select2Widget, Select2MultipleWidget

from home.models import Suburb, PricingMethod, PropertyType
from .models import Profile


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


class HousesFilterForm(forms.Form):
    """Form for user filter settings."""
    name = forms.CharField(label='Filter Name',
                           required=False)
    suburbs = forms.MultipleChoiceField(label='Area selection',
                                        required=True)
    PRICE_FROM_CHOICES = (
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
    )
    PRICE_TO_CHOICES = (
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
    )
    price_from = forms.ChoiceField(label='Price from',
                                   required=True,
                                   choices=PRICE_FROM_CHOICES,
                                   widget=Select2Widget)
    price_to = forms.ChoiceField(label='Price to',
                                 required=True,
                                 choices=PRICE_TO_CHOICES,
                                 initial=999999999,
                                 widget=Select2Widget)

    PRICING_METHODS_CHOICES = ((pricing_method.id, pricing_method.name)
                               for pricing_method in PricingMethod.objects.order_by('name'))
    pricing_methods = forms.MultipleChoiceField(label='Pricing methods',
                                                required=False,
                                                choices=PRICING_METHODS_CHOICES,
                                                widget=Select2MultipleWidget(
                                                    attrs={'data-placeholder': 'All pricing methods'}
                                                ),
                                                help_text='<a id="pricing-methods-select-all" href="#">Select all</a>')

    government_value_from = forms.ChoiceField(label='Government value from',
                                              required=True,
                                              choices=PRICE_FROM_CHOICES,
                                              widget=Select2Widget)
    government_value_to = forms.ChoiceField(label='Government value to',
                                            required=True,
                                            choices=PRICE_TO_CHOICES,
                                            initial=999999999,
                                            widget=Select2Widget)

    GOVERNMENT_VALUE_TO_PRICE_CHOICES = [
        (round(x*0.1, 1), str(round(x*0.1, 1))) for x in range(0, 21)
    ]
    GOVERNMENT_VALUE_TO_PRICE_CHOICES.append((999, '2+'))
    government_value_to_price_from = forms.ChoiceField(label='Ratio of government to price from',
                                                       required=True,
                                                       choices=GOVERNMENT_VALUE_TO_PRICE_CHOICES,
                                                       initial=0,
                                                       widget=Select2Widget)

    government_value_to_price_to = forms.ChoiceField(label='Ratio of government to price to',
                                                     required=True,
                                                     choices=GOVERNMENT_VALUE_TO_PRICE_CHOICES,
                                                     initial=999,
                                                     widget=Select2Widget)

    BEDROOMS_FROM_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    bedrooms_from = forms.ChoiceField(label='Bedrooms from',
                                      choices=BEDROOMS_FROM_CHOICES,
                                      widget=Select2Widget)

    BEDROOMS_TO_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (999, '5+'),
    )
    bedrooms_to = forms.ChoiceField(label='Bedrooms to',
                                    choices=BEDROOMS_TO_CHOICES,
                                    initial=999,
                                    widget=Select2Widget)

    BATHROOMS_FROM_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
    )
    bathrooms_from = forms.ChoiceField(label='Bathrooms from',
                                       choices=BATHROOMS_FROM_CHOICES,
                                       widget=Select2Widget)
    BATHROOMS_TO_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (999, '3+'),
    )
    bathrooms_to = forms.ChoiceField(label='Bathrooms to',
                                     choices=BATHROOMS_TO_CHOICES,
                                     initial=999,
                                     widget=Select2Widget)

    LANDAREA_FROM_CHOICES = (
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
    )
    landarea_from = forms.ChoiceField(label='Landarea from',
                                      choices=LANDAREA_FROM_CHOICES,
                                      initial=0,
                                      widget=Select2Widget)
    LANDAREA_TO_CHOICES = (
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
    )
    landarea_to = forms.ChoiceField(label='Landarea to',
                                    choices=LANDAREA_TO_CHOICES,
                                    initial=999999999,
                                    widget=Select2Widget)

    FLOORAREA_FROM_CHOICES = (
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
    )
    floorarea_from = forms.ChoiceField(label='Floorarea from',
                                       choices=FLOORAREA_FROM_CHOICES,
                                       initial=0,
                                       widget=Select2Widget)

    FLOORAREA_TO_CHOICES = (
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
    )
    floorarea_to = forms.ChoiceField(label='Floorarea to',
                                     choices=FLOORAREA_TO_CHOICES,
                                     initial=999999999,
                                     widget=Select2Widget)

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

    CARSPACE_FROM_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (999, '5+'),
    )
    carspace_from = forms.ChoiceField(label='Carspace from',
                                      choices=CARSPACE_FROM_CHOICES,
                                      initial=1,
                                      widget=Select2Widget)
    CARSPACE_TO_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (999, '5+'),
    )
    carspace_to = forms.ChoiceField(label='Carspace to',
                                    choices=CARSPACE_TO_CHOICES,
                                    initial=999,
                                    widget=Select2Widget)

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

        super(HousesFilterForm, self).__init__(*args, **kwargs)
