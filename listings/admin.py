from django.contrib import admin
from .models import HouseUserData


class HouseUserDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'house', 'user')

    search_fields = ['house__street_name', 'house__suburb__city__city_name', 'house__suburb__name', 'user__username']

    def has_add_permission(self, request):
        return False

admin.site.register(HouseUserData, HouseUserDataAdmin)
