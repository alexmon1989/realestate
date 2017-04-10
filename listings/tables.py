import django_tables2 as tables
from django_tables2 import A
from django.utils.html import format_html
from django.urls import reverse

from home.models import House, VHousesForTables

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


class NewListingsTableActionColumn(tables.Column):
    """Column type for actions (like, dislike, still thinking)."""
    def render(self, value):
        return format_html(
            '<div class="btn-group">'
            '<a href="{}?return_url={}" class="btn btn-primary"><i class="fa fa-thumbs-o-up"></i></a>'
            '<a href="{}" class="btn btn-danger"><i class="fa fa-thumbs-o-down"></i></a>'
            '<a href="{}" class="btn btn-warning"><i class="fa fa-hourglass"></i></a>'
            '</div>',
            reverse('listings:mark_as_liked', args=(value,)),
            reverse('listings:new_listing'),
            reverse('listings:mark_as_disliked', args=(value,)),
            reverse('listings:mark_as_still_thinking', args=(value,)),
        )


class NewListingsTable(tables.Table):
    address = tables.LinkColumn('listings:show_new_listing',
                                args=[A('house_id')],
                                accessor='address')
    region = tables.Column(accessor='region_name', verbose_name='Region')
    city = tables.Column(accessor='city_name', verbose_name='City')
    property_type = tables.Column(accessor='property_type_full', verbose_name='Property Type')
    price = tables.Column(accessor='price_with_price_type', verbose_name='Price', order_by='price')
    suburb = tables.Column(accessor='suburb_name', verbose_name='Suburb')
    actions = NewListingsTableActionColumn(orderable=False, accessor='house_id', verbose_name='Actions')
    create_date = tables.Column(accessor='listing_create_date', verbose_name='Listed On')

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
            'create_date',
            'actions'
        )
        attrs = {'class': 'table table-bordered table-striped table-hover'}


class NewListingsTableWithPhoto(NewListingsTable):
    photo = PhotoColumn(orderable=False, accessor='photos')

    class Meta:
        template = 'django_tables2/bootstrap.html'
        model = VHousesForTables
        fields = (
            'address',
            'property_type',
            'price',
            'create_date'
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


class LikedListingsTableActionColumn(tables.Column):
    """Column type for actions (show)."""
    def render(self, value):
        return format_html(
            '<div class="btn-group">'
            '<a href="{0}?return_url={2}" class="btn btn-danger"><i class="fa fa-thumbs-o-down"></i></a>'
            '<a href="{1}?return_url={2}" class="btn btn-warning"><i class="fa fa-hourglass"></i></a>'
            '</div>',
            reverse('listings:mark_as_disliked', args=(value,)),
            reverse('listings:mark_as_still_thinking', args=(value,)),
            reverse('listings:liked_listing'),
        )


class LikedListingsTable(tables.Table):
    region = tables.Column(accessor='house__suburb__city__region__name')
    city = tables.Column(accessor='house__suburb__city__city_name')
    suburb = tables.Column(accessor='house__suburb__name')
    address = tables.LinkColumn('listings:show_liked_listing',
                                args=[A('house_id')],
                                accessor='address')
    property_type = tables.Column(accessor='property_type')
    price = tables.Column(accessor='price_with_price_type', verbose_name='Price', order_by='price')
    create_date = tables.Column(accessor='house__listing_create_date', verbose_name='Listed On')
    actions = LikedListingsTableActionColumn(orderable=False, accessor='house_id', verbose_name='Actions')

    class Meta:
        template = 'django_tables2/bootstrap.html'
        model = House
        fields = ()
        sequence = (
            'address',
            'suburb',
            'city',
            'region',
            'property_type',
            'price',
            'create_date',
            'actions'
        )
        attrs = {'class': 'table table-bordered table-striped table-hover'}


class LikedListingsTableWithPhoto(LikedListingsTable):
    photo = PhotoColumn(orderable=False, accessor='house__photos')

    class Meta:
        template = 'django_tables2/bootstrap.html'
        model = House
        fields = ()
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


class DislikedListingsTableActionColumn(tables.Column):
    """Column type for actions (show)."""
    def render(self, value):
        return format_html(
            '<div class="btn-group">'
            '<a href="{0}?return_url={2}" class="btn btn-primary"><i class="fa fa-thumbs-o-up"></i></a>'
            '<a href="{1}?return_url={2}" class="btn btn-warning"><i class="fa fa-hourglass"></i></a>'
            '</div>',
            reverse('listings:mark_as_liked', args=(value,)),
            reverse('listings:mark_as_still_thinking', args=(value,)),
            reverse('listings:disliked_listing'),
        )


class DislikedListingsTable(LikedListingsTable):
    address = tables.LinkColumn('listings:show_disliked_listing',
                                args=[A('house_id')],
                                accessor='address')
    actions = DislikedListingsTableActionColumn(orderable=False, accessor='house_id', verbose_name='Actions')

    class Meta(LikedListingsTable.Meta):
        pass


class DislikedListingsTableWithPhoto(LikedListingsTableWithPhoto):
    address = tables.LinkColumn('listings:show_disliked_listing',
                                args=[A('house_id')],
                                accessor='address')
    actions = DislikedListingsTableActionColumn(orderable=False, accessor='house_id', verbose_name='Actions')

    class Meta(LikedListingsTableWithPhoto.Meta):
        pass


class StillThinkingListingsTableActionColumn(tables.Column):
    """Column type for actions (show)."""
    def render(self, value):
        return format_html(
            '<div class="btn-group">'
            '<a href="{0}?return_url={2}" class="btn btn-primary"><i class="fa fa-thumbs-o-up"></i></a>'
            '<a href="{1}?return_url={2}" class="btn btn-danger"><i class="fa fa-thumbs-o-down"></i></a>'
            '</div>',
            reverse('listings:mark_as_liked', args=(value,)),
            reverse('listings:mark_as_disliked', args=(value,)),
            reverse('listings:still_thinking_listing'),
        )


class StillThinkingListingsTable(LikedListingsTable):
    address = tables.LinkColumn('listings:show_still_thinking_listing',
                                args=[A('house_id')],
                                accessor='address')
    actions = StillThinkingListingsTableActionColumn(orderable=False, accessor='house_id', verbose_name='Actions')

    class Meta(LikedListingsTable.Meta):
        pass


class StillThinkingListingsTableWithPhoto(LikedListingsTableWithPhoto):
    address = tables.LinkColumn('listings:show_still_thinking_listing',
                                args=[A('house_id')],
                                accessor='address')
    actions = StillThinkingListingsTableActionColumn(orderable=False, accessor='house_id', verbose_name='Actions')

    class Meta(LikedListingsTableWithPhoto.Meta):
        pass
