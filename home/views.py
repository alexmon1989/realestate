from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from decorators import group_required

from listings.models import MarkedHouse
from home.models import VHousesForTables


@login_required
@group_required('Users')
def dashboard(request):
    """Shows dashboard page."""
    filters = request.user.housesfilter_set.filter(disabled=False).all()

    # get new houses queryset
    excluded_pks = [h.house_id for h in MarkedHouse.objects.filter(user=request.user).only('house_id')]
    new_houses_count = len(VHousesForTables.get_new_houses(filters, excluded_pks))

    # get liked, still thinking count
    liked_count = MarkedHouse.objects.filter(user=request.user, mark_id=1).count()
    still_thinking_count = MarkedHouse.objects.filter(user=request.user, mark_id=3).count()

    return render(request, 'home/dashboard.html', {
        'new_count': new_houses_count,
        'liked_count': liked_count,
        'still_thinking_count': still_thinking_count
    })
