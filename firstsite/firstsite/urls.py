from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('finder.urls')),
    url(r'^finder/', include('finder.urls')),
    url(r'^historic/', include('historic.urls')),
    url(r'^admin/', admin.site.urls),
    ]
