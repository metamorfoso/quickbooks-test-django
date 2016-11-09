from django.conf.urls import url
from . import views

app_name = 'connector'
urlpatterns = [
    url(r'^qb_connect/$', views.qb_connect, name='qb_connect'),
    url(r'^qb_callback/$', views.qb_callback, name='qb_callback'),
    url(r'^qb_disconnect/$', views.qb_disconnect, name='qb_disconnect')
]
