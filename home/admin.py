from django.contrib import admin
from .models import House, Agency, City, Agent


class HouseAdmin(admin.ModelAdmin):
    """Admin model for House objects."""
    search_fields = (
        'street_name',
        'suburb__city__city_name',
        'suburb__name',
        'suburb__city__region__name',
        'property_type__name',
        'price_type__name'
    )

    list_display = ('get_address', 'suburb', 'get_city', 'get_region', 'get_property_type', 'get_price')

    list_filter = ('suburb__city__city_name', 'suburb__city__region__name')


class AgencyAdmin(admin.ModelAdmin):
    """Admin model for Agency objects."""
    search_fields = ['agency_name', 'city__city_name', 'email', 'work_phone']

    list_display = ('agency_name', 'city', 'email', 'work_phone')

    list_filter = ('city__city_name',)


class CityAdmin(admin.ModelAdmin):
    """Admin model for City objects."""
    search_fields = ('city_name', 'region__name', 'capital_growth', 'council_link')

    list_display = ('city_name', 'region', 'capital_growth', 'council_link')

    list_filter = ('region__name', )


class AgentAdmin(admin.ModelAdmin):
    """Admin model for Agent objects."""
    search_fields = ('name', 'mobile_phone', 'ddi_phone', 'work_phone', 'email', 'agency__agency_name')

    list_display = ('name', 'mobile_phone', 'ddi_phone', 'work_phone', 'email', 'agency')

    readonly_fields = ('houses', )


admin.site.register(House, HouseAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Agent, AgentAdmin)
