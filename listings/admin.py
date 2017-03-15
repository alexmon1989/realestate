from django.contrib import admin
from .models import HouseUserData


class HouseUserDataAdmin(admin.ModelAdmin):
    """Admin model for House user data objects."""
    list_display = ('id', 'house', 'user')
    list_display_links = ('id', )

    readonly_fields = ('house', 'user')

    search_fields = ['house__street_name', 'house__suburb__city__city_name', 'house__suburb__name', 'user__username']

    def has_add_permission(self, request):
        return False

admin.site.register(HouseUserData, HouseUserDataAdmin)
