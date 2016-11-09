from django.conf.urls import url
from . import views

app_name = 'explorer'
urlpatterns = [
    url(r'^$', views.index, name='landing_page'),
    url(r'^qb_connect/$', views.qb_connect, name='qb_connect'),
    url(r'^qb_callback/$', views.qb_callback, name='qb_callback'),
    url(r'^qb_disconnect/$', views.qb_disconnect, name='qb_disconnect'),
    url(r'^browse/(?P<entity>[\w-]+)/$', views.browse, name='browse'),
    url(r'^single_entity/(?P<entity>[\w-]+)/(?P<entity_id>[\w-]+)/$', views.single_entity, name='single_entity'),
    url(r'^query/$', views.query, name='query'),
    url(r'^read/$', views.read, name='read'),
    url(r'^update/$', views.update, name='update'),
    url(r'^create/$', views.create, name='create')
]
