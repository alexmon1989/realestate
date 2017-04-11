from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^settings/$', views.profile, name='profile'),
    url(r'^settings/house-filters/$', views.house_filters, name='house_filters'),
    url(r'^settings/change-password/$', views.change_password, name='change_password'),
    url(r'^settings/users-constants/$', views.users_constants, name='users_constants'),
    url(r'^settings/region-and-cities-constants/$',
        views.region_and_cities_constants,
        name='region_and_cities_constants'),
    url(r'^settings/filters/create/$', views.create_filter, name='create_filter'),
    url(r'^settings/filters/edit/(?P<pk>[0-9]+)/$', views.edit_filter, name='edit_filter'),
    url(r'^settings/filters/delete/(?P<pk>[0-9]+)/$', views.FilterDeleteView.as_view(), name='delete_filter'),
    url(r'^settings/change-show-title-photo/$', views.change_show_title_photo, name='change_show_title_photo'),
    url(r'^settings/change-font-size/$', views.change_font_size, name='change_font_size'),
    url(r'^settings/filters/toggle-disabled/(?P<pk>[0-9]+)/$', views.toggle_disabled, name='toggle_disabled'),
    url(r'^settings/users-constants/get-capital-growth/(?P<city_id>[0-9]+)/$',
        views.get_capital_growth,
        name='get_capital_growth'),
]
