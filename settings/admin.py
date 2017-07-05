from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from .models import Global, MotdBanner


class DeleteNotAllowedModelAdmin(SingleModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Global, DeleteNotAllowedModelAdmin)
admin.site.register(MotdBanner, DeleteNotAllowedModelAdmin)
