from django.conf.urls import patterns, include, url

from django.contrib import admin
from views import *
admin.autodiscover()

urlpatterns = patterns('',
    (r'^register/$', register),
    (r'^login/$', login),
    (r'^view_profile/$', view_profile),
#    url(r'^admin/', include(admin.site.urls)),
)
