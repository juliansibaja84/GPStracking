from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^req/all/', views.req),
    url(r'^req/one/', views.reqOne),
    url(r'^req/oneanother/', views.reqOneAnother),
]
