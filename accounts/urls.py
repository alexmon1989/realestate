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
]
