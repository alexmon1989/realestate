from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget

from home.models import Suburb, PricingMethod, PropertyType


class SearchForm(forms.Form):
    """Form for search houses."""
    suburbs = forms.MultipleChoiceField(label='Area selection',
                                        required=False)
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
                                   required=False,
                                   initial=0,
                                   choices=PRICE_FROM_CHOICES,
                                   widget=Select2Widget)
    price_to = forms.ChoiceField(label='Price to',
                                 required=False,
                                 choices=PRICE_TO_CHOICES,
                                 initial=999999999,
                                 widget=Select2Widget)

    PRICING_METHODS_CHOICES = ((pricing_method.id, pricing_method.name)
                               for pricing_method in PricingMethod.objects.order_by('name'))
    pricing_methods = forms.MultipleChoiceField(label='Pricing methods',
                                                required=False,
                                                choices=PRICING_METHODS_CHOICES,
                                                widget=Select2MultipleWidget,
                                                help_text='<a id="pricing-methods-select-all" href="#">Select all</a>')

    BEDROOMS_FROM_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    bedrooms_from = forms.ChoiceField(label='Bedrooms from',
                                      required=False,
                                      initial=1,
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
                                    required=False,
                                    choices=BEDROOMS_TO_CHOICES,
                                    initial=999,
                                    widget=Select2Widget)

    BATHROOMS_FROM_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
    )
    bathrooms_from = forms.ChoiceField(label='Bathrooms from',
                                       required=False,
                                       initial=1,
                                       choices=BATHROOMS_FROM_CHOICES,
                                       widget=Select2Widget)
    BATHROOMS_TO_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (999, '3+'),
    )
    bathrooms_to = forms.ChoiceField(label='Bathrooms to',
                                     required=False,
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
                                      required=False,
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
                                    required=False,
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
                                       required=False,
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
                                     required=False,
                                     choices=FLOORAREA_TO_CHOICES,
                                     initial=999999999,
                                     widget=Select2Widget)

    PROPERTY_TYPE_CHOICES = ((property_type.id, property_type.name)
                             for property_type in PropertyType.objects.order_by('name'))
    property_type = forms.MultipleChoiceField(label='Property type',
                                              required=False,
                                              choices=PROPERTY_TYPE_CHOICES,
                                              widget=Select2MultipleWidget,
                                              help_text='<a id="property-type-select-all" href="#">Select all</a>')
    show_only_open_homes = forms.BooleanField(label='Show only open homes', required=False)
    show_only_properties_with_address = forms.BooleanField(label='Show only properties with an address', required=False)
    keywords = forms.CharField(label='Keywords', required=False)
    listings_age_days = forms.IntegerField(
        label='Listings age (days), not more',
        required=True,
        initial=14,
        min_value=0
    )

    def __init__(self, *args, **kwargs):
        suburbs = [(suburb['id'], suburb['name'])
                   for suburb
                   in Suburb.objects.values('id', 'name').order_by('city__region__name', 'city__city_name', 'name')]
        self.base_fields['suburbs'].choices = suburbs

        super(SearchForm, self).__init__(*args, **kwargs)
