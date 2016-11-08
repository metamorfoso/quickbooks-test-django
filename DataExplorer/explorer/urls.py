from django.conf.urls import url
from . import views

app_name = 'explorer'
urlpatterns = [
    url(r'^$', views.index, name='landing_page'),
    url(r'^qb_connect/$', views.qb_connect, name='qb_connect'),
    url(r'^qb_callback/$', views.qb_callback, name='qb_callback'),
    url(r'^qb_disconnect/$', views.qb_disconnect, name='qb_disconnect'),
    url(r'^all_accounts/$', views.all_accounts, name='all_accounts'),
    url(r'^single_account/(?P<account_id>[\w-]+)$', views.single_account, name='single_account')
]
