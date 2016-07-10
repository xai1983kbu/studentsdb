from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    # Students urls
    url(r'^$','students.views.students_list', name='home'),
    url(r'^students/add/?$','students.views.students_add', name='students_add'),
    url(r'^students/(?P<sid>[0-9]+)/edit/?$','students.views.students_edit', name='students_edit'),
    url(r'^students/(?P<sid>[0-9]+)/delete/?$','students.views.students_delete', name='students_delete'),
    
    # Groups urls
    url(r'^mygroups/$', 'students.views.groups_list', name='groups'),
    url(r'^groups/add/?$','students.views.groups_add', name='groups_add'),
    url(r'^groups/(?P<gid>[0-9]+)/edit/?$','students.views.groups_edit', name='groups_edit'),
    url(r'^groups/(?P<gid>[0-9]+)/delete/?$','students.views.groups_delete', name='groups_delete'),


    url(r'^admin/', admin.site.urls),
]
