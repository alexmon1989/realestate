from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/save-user-data/$', views.save_user_data, name='save_user_data'),
    url(r'^profile/change-password/$', views.change_password, name='change_password'),
]
