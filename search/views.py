from django.shortcuts import render
from django_tables2 import RequestConfig
from .forms import SearchForm
from home.models import House
from listings.tables import NewListingsTableWithPhoto


def index(request):
    """Shows search page and search results."""
    houses = []

    if request.GET:
        form = SearchForm(request.GET)
        houses = House.search(request.GET)
    else:
        form = SearchForm()

    table = NewListingsTableWithPhoto(houses)
    RequestConfig(request).configure(table)

    return render(request, 'search/index.html', {
        'form': form,
        'table': table,
        'total': len(houses)
    })
