import django_tables2 as tables
from django.utils.html import format_html
from django.urls import reverse

from home.models import House

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
                i = i + 1
            return html
        return ''


class NewListingsTableActionColumn(tables.Column):
    """Column type for actions (like, dislike, still thinking)."""
    def render(self, value):
        return format_html(
            '<div class="btn-group">'
            '<a href="{}" class="btn btn-primary"><i class="fa fa-thumbs-o-up"></i></a>'
            '<a href="{}" class="btn btn-danger"><i class="fa fa-thumbs-o-down"></i></a>'
            '<a href="{}" class="btn btn-warning"><i class="fa fa-hourglass"></i></a>'
            '</div>',
            reverse('listings:mark_as_liked', args=(value,)),
            reverse('listings:mark_as_disliked', args=(value,)),
            reverse('listings:mark_as_still_thinking', args=(value,)),
        )


class DetailsNewListingsColumn(tables.Column):
    """Column type with house id as link to house's page."""
    def render(self, value):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('listings:show_new_listing', args=(value,)),
            value
        )


class NewListingsTable(tables.Table):
    house_id = DetailsNewListingsColumn(accessor='house_id')
    address = tables.Column(accessor='address')
    region = tables.Column(accessor='suburb__city__region__name')
    city = tables.Column(accessor='suburb__city__city_name')
    suburb = tables.Column(accessor='suburb__name')
    actions = NewListingsTableActionColumn(orderable=False, accessor='house_id', verbose_name='Actions')
    create_date = tables.Column(accessor='listing_create_date', verbose_name='Listed On')

    class Meta:
        template = 'django_tables2/bootstrap.html'
        model = House
        fields = (
            'house_id',
            'address',
            'land',
            'floor',
            'price',
            'create_date',
        )
        sequence = (
            'house_id',
            'address',
            'suburb',
            'city',
            'region',
            'land',
            'floor',
            'price',
            'create_date',
            'actions'
        )
        attrs = {'class': 'table table-bordered table-striped table-hover'}


class NewListingsTableWithPhoto(NewListingsTable):
    photo = PhotoColumn(orderable=False, accessor='photos')

    class Meta:
        template = 'django_tables2/bootstrap.html'
        model = House
        fields = (
            'house_id',
            'address',
            'land',
            'floor',
            'price',
            'create_date'
        )
        sequence = (
            'house_id',
            'address',
            'suburb',
            'city',
            'region',
            'land',
            'floor',
            'price',
            'photo',
            'create_date',
            'actions'
        )
        attrs = {'class': 'table table-bordered table-striped table-hover'}


class DetailsLikedListingsColumn(tables.Column):
    """Column type with house id as link to house's page."""
    def render(self, value):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('listings:show_liked_listing', args=(value,)),
            value
        )


class LikedListingsTableActionColumn(tables.Column):
    """Column type for actions (show)."""
    def render(self, value):
        return format_html(
            '<div class="btn-group">'
            '<a href="{}" class="btn btn-danger"><i class="fa fa-thumbs-o-down"></i></a>'
            '<a href="{}" class="btn btn-warning"><i class="fa fa-hourglass"></i></a>'
            '</div>',
            reverse('listings:mark_as_disliked', args=(value,)),
            reverse('listings:mark_as_still_thinking', args=(value,)),
        )


class LikedListingsTable(tables.Table):
    house_id = DetailsLikedListingsColumn(accessor='house_id')
    region = tables.Column(accessor='house__suburb__city__region__name')
    city = tables.Column(accessor='house__suburb__city__city_name')
    suburb = tables.Column(accessor='house__suburb__name')
    address = tables.Column(accessor='address')
    land = tables.Column(accessor='house__land')
    floor = tables.Column(accessor='house__floor')
    price = tables.Column(accessor='house__price')
    create_date = tables.Column(accessor='house__listing_create_date', verbose_name='Listed On')
    actions = LikedListingsTableActionColumn(orderable=False, accessor='house_id', verbose_name='Actions')

    class Meta:
        template = 'django_tables2/bootstrap.html'
        model = House
        fields = (
            'house_id',
        )
        sequence = (
            'house_id',
            'address',
            'suburb',
            'city',
            'region',
            'land',
            'floor',
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
        fields = (
            'house_id',
        )
        sequence = (
            'house_id',
            'address',
            'suburb',
            'city',
            'region',
            'land',
            'floor',
            'price',
            'photo',
            'create_date',
            'actions'
        )
        attrs = {'class': 'table table-bordered table-striped table-hover'}


class DetailsDislikedListingsColumn(tables.Column):
    """Column type with house id as link to house's page."""
    def render(self, value):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('listings:show_disliked_listing', args=(value,)),
            value
        )


class DislikedListingsTableActionColumn(tables.Column):
    """Column type for actions (show)."""
    def render(self, value):
        return format_html(
            '<div class="btn-group">'
            '<a href="{}" class="btn btn-primary"><i class="fa fa-thumbs-o-up"></i></a>'
            '<a href="{}" class="btn btn-warning"><i class="fa fa-hourglass"></i></a>'
            '</div>',
            reverse('listings:mark_as_liked', args=(value,)),
            reverse('listings:mark_as_disliked', args=(value,)),
            reverse('listings:mark_as_still_thinking', args=(value,)),
        )


class DislikedListingsTable(LikedListingsTable):
    house_id = DetailsDislikedListingsColumn(accessor='house_id')
    actions = DislikedListingsTableActionColumn(orderable=False, accessor='house_id', verbose_name='Actions')

    class Meta(LikedListingsTable.Meta):
        pass


class DislikedListingsTableWithPhoto(LikedListingsTableWithPhoto):
    house_id = DetailsDislikedListingsColumn(accessor='house_id')
    actions = DislikedListingsTableActionColumn(orderable=False, accessor='house_id', verbose_name='Actions')

    class Meta(LikedListingsTableWithPhoto.Meta):
        pass


class StillThinkingListingsTableActionColumn(tables.Column):
    """Column type for actions (show)."""
    def render(self, value):
        return format_html(
            '<div class="btn-group">'
            '<a href="{}" class="btn btn-primary"><i class="fa fa-thumbs-o-up"></i></a>'
            '<a href="{}" class="btn btn-danger"><i class="fa fa-thumbs-o-down"></i></a>'
            '</div>',
            reverse('listings:mark_as_liked', args=(value,)),
            reverse('listings:mark_as_disliked', args=(value,)),
            reverse('listings:mark_as_still_thinking', args=(value,)),
        )


class DetailsStillThinkingListingsColumn(tables.Column):
    """Column type with house id as link to house's page."""
    def render(self, value):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('listings:show_still_thinking_listing', args=(value,)),
            value
        )


class StillThinkingListingsTable(LikedListingsTable):
    house_id = DetailsStillThinkingListingsColumn(accessor='house_id')
    actions = StillThinkingListingsTableActionColumn(orderable=False, accessor='house_id', verbose_name='Actions')

    class Meta(LikedListingsTable.Meta):
        pass


class StillThinkingListingsTableWithPhoto(LikedListingsTableWithPhoto):
    house_id = DetailsStillThinkingListingsColumn(accessor='house_id')
    actions = StillThinkingListingsTableActionColumn(orderable=False, accessor='house_id', verbose_name='Actions')

    class Meta(LikedListingsTableWithPhoto.Meta):
        pass
