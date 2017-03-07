from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/save-user-data/$', views.save_user_data, name='save_user_data'),
    url(r'^profile/change-password/$', views.change_password, name='change_password'),
    url(r'^profile/filters/create/$', views.create_filter, name='create_filter'),
    url(r'^profile/filters/edit/(?P<pk>[0-9]+)/$', views.edit_filter, name='edit_filter'),
    url(r'^profile/filters/delete/(?P<pk>[0-9]+)/$', views.FilterDeleteView.as_view(), name='delete_filter'),
    url(r'^profile/change-show-title-photo/$', views.change_show_title_photo, name='change_show_title_photo'),
    url(r'^profile/change-font-size/$', views.change_font_size, name='change_font_size'),
]
