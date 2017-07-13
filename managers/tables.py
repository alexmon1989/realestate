import django_tables2 as tables
from django.utils.html import format_html
from django.urls import reverse

from managers.models import Manager


class ActionColumn(tables.Column):
    """Column type for actions (like, dislike, still thinking)."""
    def render(self, value):
        return format_html(
            '<div class="btn-group">'
            '<a href="{}" class="btn btn-primary" title="Edit"><i class="fa fa-edit"></i></a>'
            '<a href="{}" class="btn btn-danger" title="Remove"><i class="fa fa-remove"></i></a>'
            '</div>',
            reverse('managers:manager_edit', args=(value,)),
            reverse('managers:manager_delete', args=(value,)),
        )


class ManagerTable(tables.Table):
    actions = ActionColumn(orderable=False, accessor='id', verbose_name='Actions')

    class Meta:
        model = Manager
        fields = (
            'name',
            'agency',
            'phone_numbers',
            'email',
            'rate',
            'city',
            'created_at',
            'updated_at',
        )
        attrs = {'class': 'table table-bordered table-striped table-hover'}
