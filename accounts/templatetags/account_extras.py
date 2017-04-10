from django import template
from django.core.cache import cache

from home.models import Suburb

register = template.Library()


@register.simple_tag
def get_full_suburb_path(suburb_id):
    """Returns suburbs paths in format 'Region/City'."""
    suburb_paths = cache.get('suburb_paths', {})
    if suburb_paths == {}:
        suburbs = Suburb.objects.values('id', 'city__region__name', 'city__city_name', 'name')\
            .order_by('city__region__name', 'city__city_name', 'name')
        for suburb in suburbs:
            suburb_paths[suburb['id']] = \
                "{}/{}".format(suburb['city__region__name'].replace('/', '&frasl;'), suburb['city__city_name'])
        cache.set('suburb_paths', suburb_paths)

    return suburb_paths[suburb_id]


@register.inclusion_tag('accounts/fonts_sizes.html', takes_context=True)
def font_sizes(context):
    """Returns js-code for change font size."""
    return {
        'ratio': context['request'].user.profile.font_ratio
    }
