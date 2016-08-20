from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^finder/', include('finder.urls')),
    url(r'^admin/', admin.site.urls),
    ]
