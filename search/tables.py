import django_tables2 as tables
from django_tables2 import A
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.sessions.backends.db import SessionStore

from home.models import VHousesForTables

import random
import string


class PhotoColumn(tables.Column):
    """Column type for photo column."""
    def render(self, value):
        photos = value.split(';')
        photos_len = len(photos)
        random_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        if photos_len > 0:
            html = format_html(
                '<a href="{0}" data-lightbox="{1}"><img class="attachment-img" src="{0}" /></a>',
                photos[0],
                random_str
            )
            i = 1
            while i < photos_len:
                html = html + format_html(
                    '<a href="{0}" data-lightbox="{1}"></a>',
                    photos[i],
                    random_str
                )
                i += 1
            return html
        return ''


class ListingsTableActionColumn(tables.Column):
    """Column type for actions (like, dislike, still thinking)."""
    def render(self, value):
        return format_html(
            '<div class="btn-group">'
            '<a href="{}?return_url=search" class="btn btn-primary"><i class="fa fa-plus"></i></a>'
            '<a href="{}?return_url=search"" class="btn btn-danger"><i class="fa fa-minus"></i></a>'
            '<a href="{}?return_url=search"" class="btn btn-warning"><i class="fa fa-hourglass"></i></a>'
            '</div>',
            reverse('listings:mark_as_liked', args=(value,)),
            reverse('listings:mark_as_disliked', args=(value,)),
            reverse('listings:mark_as_still_thinking', args=(value,)),
        )


class AddressLink(tables.LinkColumn):
    def render(self, value, record, bound_column):
        def resolve_if_accessor(val):
            return val.resolve(record) if isinstance(val, A) else val

        params = {}
        if self.args:
            params['args'] = [resolve_if_accessor(a) for a in self.args]

        return format_html(
            '<a href="{}?return_url=search">{}</a>',
            reverse('listings:show_new_listing', args=params['args']),
            value
        )


class ListingsTable(tables.Table):
    address = AddressLink('listings:show_new_listing',
                                args=[A('house_id')],
                                accessor='address')
    region = tables.Column(accessor='region_name', verbose_name='Region')
    city = tables.Column(accessor='city_name', verbose_name='City')
    property_type = tables.Column(accessor='property_type_full', verbose_name='Property Type')
    price = tables.Column(accessor='price_with_price_type', verbose_name='Price', order_by='price')
    suburb = tables.Column(accessor='suburb_name', verbose_name='Suburb')
    create_date = tables.Column(accessor='listing_create_date', verbose_name='Listed On')
    photo = PhotoColumn(orderable=False, accessor='photos')
    actions = ListingsTableActionColumn(
        orderable=False,
        accessor='house_id',
        verbose_name='Actions',
    )

    class Meta:
        template = 'django_tables2/bootstrap.html'
        model = VHousesForTables
        fields = (
            'address',
            'property_type',
            'price',
            'create_date',
        )
        sequence = (
            'address',
            'suburb',
            'city',
            'region',
            'property_type',
            'price',
            'photo',
            'create_date',
            'actions'
        )
        attrs = {'class': 'table table-bordered table-striped table-hover'}
