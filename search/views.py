from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig
from .forms import SearchForm
from home.models import VHousesForTables
from search.tables import ListingsTable

from decorators import group_required


@login_required
@group_required(('Users', 'Self'))
def index(request):
    """Shows search page and search results."""
    houses = []

    if request.GET:
        request.session['search_uri'] = request.get_full_path()
        form = SearchForm(data=request.GET)
        houses = VHousesForTables.search(request.GET)
    else:
        form = SearchForm()

    table = ListingsTable(houses)
    RequestConfig(request).configure(table)

    return render(request, 'search/index.html', {
        'form': form,
        'table': table,
        'total': len(table.rows)
    })
