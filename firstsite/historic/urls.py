from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^req/(?P<lower>.+)/(?P<upper>.+)/$', views.getPoints),
    url(r'^rq/(?P<latit>.+)/(?P<longit>.+)/(?P<lower>.+)/(?P<upper>.+)/$', views.getPointsT),
    url(r'^reqanother/(?P<lower>.+)/(?P<upper>.+)/$', views.getPointsAnother),
    url(r'^rqanother/(?P<latit>.+)/(?P<longit>.+)/(?P<lower>.+)/(?P<upper>.+)/$', views.getPointsTAnother),
    url(r'stats/', views.statsRequests),
    url(r'^savep/$', views.savePos),
]
