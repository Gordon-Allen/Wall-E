from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^wall$', views.wall),
    url(r'^login$', views.login),
    url(r'^log_out$', views.log_out),
    url(r'^add_message$', views.add_message),
    url(r'^add_comment$', views.add_comment),
    url(r'^message/delete/(?P<id>\d+)$', views.delete),
    url(r'^comment/delete/(?P<id>\d+)$', views.dcomment),
]