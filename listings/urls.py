from django.conf.urls import url

from . import views

app_name = 'listings'
urlpatterns = [
    url(r'^new/$', views.new_listings, name='new_listing'),
    url(r'^liked/$', views.liked_listings, name='liked_listing'),
    url(r'^disliked/$', views.disliked_listings, name='disliked_listing'),
    url(r'^still-thinking/$', views.still_thinking_listings, name='still_thinking_listing'),
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
]
