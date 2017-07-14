from django.conf.urls import url

from managers.views import *

app_name = 'managers'
urlpatterns = [
    url(r'^$', ManagerList.as_view(), name='manager_list'),
    url(r'^create/$', ManagerCreate.as_view(), name='manager_create'),
    url(r'^edit/(?P<pk>\d+)/$', ManagerEdit.as_view(), name='manager_edit'),
    url(r'^delete/(?P<pk>\d+)/$', ManagerDelete.as_view(), name='manager_delete'),
    url(r'^create-manager-ajax/$', add_manager_ajax, name='add_manager_ajax'),
]
