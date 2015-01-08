from django.conf.urls import patterns, include, url

from django.contrib import admin
from views import *
admin.autodiscover()


urlpatterns = patterns('',
    (r'^register/$', register),
    (r'^login/$', login),
    (r'^view_profile/$', view_profile),
    (r'^project_all/$', project_all),
    #url(r'^admin/', include(admin.site.urls)),
    #(r'^projectInfo/$', projectInfo),
    #(r'^project_users/$', project_users),
    #(r'^project_tasks/$', project_tasks),
    (r'^taskInfo/$', taskInfo),
    (r'^addMember/$', addMember),
    (r'^addProject/$', addProject),
    (r'^addTask/$', addTask),
    (r'^deleteProject/$', deleteProject),
    (r'^editProject/$', editProject),
    (r'^editTask/$', editTask),
    (r'^deleteTask/$', deleteTask),
    (r'^deleteMember/$', deleteMember),
    (r'^changeStatus/$', changeStatus),
    (r'^changePassword/$', changePassword),
    (r'^deleteAccount/$', deleteAccount),
    (r'^gcmDatabase/$', gcmDatabase),
    (r'^signOut/$', signOut)
)
