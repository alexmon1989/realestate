from django import template

from settings.models import MotdBanner

register = template.Library()


@register.inclusion_tag('settings/motd.html')
def motd_banner():
    motd = MotdBanner.objects.get()
    return {
        'enabled': motd.enabled,
        'message': motd.message
    }
