from django.conf.urls import patterns, include, url

from django.contrib import admin
from views import *
admin.autodiscover()

urlpatterns = patterns('',
    (r'^register/$', register),
    (r'^login/$', login),
    (r'^view_profile/$', view_profile),
    (r'^projectInfo/$', projectInfo),
    (r'^project_users/$', project_users),
    (r'^project_tasks/$', project_tasks),
    (r'^taskInfo/$', taskInfo),
    (r'^addMember/$', addMember),
    (r'^addProject/$', addProject),
    (r'^addTask/$', addTask)
#    url(r'^admin/', include(admin.site.urls)),
)
