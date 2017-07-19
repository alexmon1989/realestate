from django.conf.urls import url

from . import views

app_name = 'listings'
urlpatterns = [
    url(r'^new/$', views.new_listings, name='new_listing'),
    url(r'^liked/$', views.liked_listings, name='liked_listing'),
    url(r'^disliked/$', views.disliked_listings, name='disliked_listing'),
    url(r'^still-thinking/$', views.still_thinking_listings, name='still_thinking_listing'),
    url(r'^my-listings/$', views.UsersHousesListView.as_view(), name='my_listing'),
    url(r'^my-listings/create/$', views.HouseCreateView.as_view(), name='my_listing_create'),
    url(r'^my-listings/delete/(?P<pk>[0-9]+)/$', views.HouseDeleteView.as_view(), name='my_listing_delete'),
    url(r'^my-listings/edit/(?P<pk>[0-9]+)/$', views.HouseUpdateView.as_view(), name='my_listing_update'),
    url(r'^new/show/(?P<pk>[0-9]+)/$', views.show_new_listing, name='show_new_listing'),
    url(r'^liked/show/(?P<pk>[0-9]+)/$', views.show_liked_listing, name='show_liked_listing'),
    url(r'^disliked/show/(?P<pk>[0-9]+)/$', views.show_disliked_listing, name='show_disliked_listing'),
    url(
        r'^still-thinking/show/(?P<pk>[0-9]+)/$',
        views.show_still_thinking_listing,
        name='show_still_thinking_listing'
    ),
    url(r'^mark-as-liked/(?P<pk>[0-9]+)/$', views.mark_as_liked, name='mark_as_liked'),
    url(r'^mark-as-disliked/(?P<pk>[0-9]+)/$', views.mark_as_disliked, name='mark_as_disliked'),
    url(r'^mark-as-still-thinking/(?P<pk>[0-9]+)/$', views.mark_as_still_thinking, name='mark_as_still_thinking'),
    url(r'^save-calculator-data/(?P<house_id>[0-9]+)/$', views.save_calculator_data, name='save_calculator_data'),
    url(r'^reset-calculator-data/(?P<house_id>[0-9]+)/$', views.reset_calculator_data, name='reset_calculator_data'),
    url(
        r'^liked/delete-other-expenses-item/(?P<pk>[0-9]+)/$',
        views.delete_other_expenses_item,
        name='delete_other_expenses_item'
    ),
    url(r'^liked/create-other-expenses-item/$', views.create_other_expenses_item, name='create_other_expenses_item'),
    url(r'^get-deposit-values/$', views.get_deposit_values, name='get_deposit_values'),
    url(r'^get-cities-by-region/(?P<region_id>[0-9]+)/$', views.get_cities_by_region, name='get_cities_by_region'),
    url(r'^get-suburbs-by-city/(?P<city_id>[0-9]+)/$', views.get_suburbs_by_city, name='get_suburbs_by_city'),
    url(r'^delete-house-photo/(?P<house_id>[0-9]+)/$', views.delete_house_photo, name='delete_house_photo'),
]
