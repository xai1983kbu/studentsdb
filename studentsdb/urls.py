from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG

urlpatterns = [
    # Students urls
    url(r'^$','students.views.students.students_list', name='home'),
    url(r'^students/add/?$','students.views.students.students_add', name='students_add'),
    url(r'^students/(?P<sid>[0-9]+)/edit/?$','students.views.students.students_edit', name='students_edit'),
    url(r'^students/(?P<sid>[0-9]+)/delete/?$','students.views.students.students_delete', name='students_delete'),
    
    # Groups urls
    url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
    url(r'^groups/add/?$','students.views.groups.groups_add', name='groups_add'),
    url(r'^groups/(?P<gid>[0-9]+)/edit/?$','students.views.groups.groups_edit', name='groups_edit'),
    url(r'^groups/(?P<gid>[0-9]+)/delete/?$','students.views.groups.groups_delete', name='groups_delete'),

    # Journal urls
    url(r'^journal/$','students.views.journal.journal', name='journal'),
    url(r'^journal/(?P<year>[0-9]+)/(?P<month>[0-9]+)/?$','students.views.journal.journal', name='journal_year_month'),
    url(r'^journal/(?P<sid>[0-9]+)/?$','students.views.journal.journal_student', name='journal_student'),

    url(r'^admin/', admin.site.urls),
]

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}))

