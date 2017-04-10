from django.utils.html import format_html
from django.urls import reverse
import django_tables2 as tables


class ActionColumn(tables.Column):
    """Column type for actions (delete, edit)."""
    def render(self, value):
        return format_html('<div class="btn-group">'
                           '<a class="btn btn-primary" href="{}"><i class="fa fa-pencil" aria-hidden="true"></i></a>'
                           '<a class="btn btn-danger" href="{}"><i class="fa fa-trash" aria-hidden="true"></i></a>'
                           '</div>',
                           reverse('accounts:edit_filter', args=(value,)),
                           reverse('accounts:delete_filter', args=(value,)))


class DisabledColumn(tables.Column):
    """Column type for disabled field."""
    def render(self, value):
        if value:
            return format_html('<a href="#"><span class="true">✔</span></a>')
        return format_html('<a href="#"><span class="false">✘</span></a>')


class FiltersTable(tables.Table):
    """Table for user's filters."""
    id = tables.Column(orderable=False)
    name = tables.Column(orderable=False, verbose_name='Filter Name')
    suburbs = tables.Column(orderable=False)
    price_from = tables.Column(orderable=False)
    price_to = tables.Column(orderable=False)
    landarea_from = tables.Column(orderable=False)
    landarea_to = tables.Column(orderable=False)
    property_type = tables.Column(orderable=False)
    disabled = DisabledColumn(orderable=False)
    created_at = tables.DateTimeColumn(orderable=False)
    updated_at = tables.DateTimeColumn(orderable=False)
    actions = ActionColumn(orderable=False)

    class Meta:
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}
