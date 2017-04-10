from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig
from .forms import SearchForm
from home.models import VHousesForTables
from listings.tables import NewListingsTableWithPhoto

from decorators import group_required


@login_required
@group_required('Users')
def index(request):
    """Shows search page and search results."""
    houses = []

    if request.GET:
        form = SearchForm(request.GET)
        houses = VHousesForTables.search(request.GET)
    else:
        form = SearchForm()

    table = NewListingsTableWithPhoto(houses)
    RequestConfig(request).configure(table)

    return render(request, 'search/index.html', {
        'form': form,
        'table': table,
        'total': len(table.rows)
    })
