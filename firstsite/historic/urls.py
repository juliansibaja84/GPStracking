from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^req/(?P<lower>.+)/(?P<upper>.+)/$', views.getPoints),
    url(r'^rq/(?P<latit>.+)/(?P<longit>.+)/(?P<lower>.+)/(?P<upper>.+)/$', views.getPointsT),
]
