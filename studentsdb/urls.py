from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG

from students.views.students_class_view import StudentList
from students.views.students import StudentUpdateView, StudentDeleteView
from students.views.students import ManyStudentDeleteView
from students.views.groups import GroupAddView, GroupUpdateView, GroupDeleteView
from students.models.groups import Group

urlpatterns = [
    # Students urls
    url(r'^$','students.views.students.students_list', name='home'),
    url(r'^students/add/?$','students.views.students_add.students_add', name='students_add'),
    url(r'^students/(?P<pk>[0-9]+)/edit/?$',StudentUpdateView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>[0-9]+)/delete/?$',StudentDeleteView.as_view(), name='students_delete'),
    url(r'^students/manydelete/?$',ManyStudentDeleteView.as_view(), name='many_students_delete'),
    url(r'^students_list/$',StudentList.as_view(), name='students_list_class_view'), # з використанням класу в'юшки 

    # Students Load More urls
    url(r'^students_load_more/?$','students.views.homeworks.students_load_more.students_list_load_more', name='students_load_more'),
    # Students Scroll urls
    url(r'^students_scroll/?$','students.views.homeworks.students_scroll.students_scroll', name='students_scroll'),

    # Groups urls
  # url(r'^groups/(?P<pk>[0-9]+)/delete/?$',StudentDeleteView.as_view( \
  #     model=Group, success_url='groups', success_message='Групу %s успішно видалено!'), name='groups_delete'),
    url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
    url(r'^groups/add/$', GroupAddView.as_view(), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(),
         name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(),
         name='groups_delete'),

    # Journal urls
    url(r'^journal/$','students.views.journal.journal', name='journal'),
    url(r'^journal/(?P<year>[0-9]+)/(?P<month>[0-9]+)/?$','students.views.journal.journal', name='journal_year_month'),
    url(r'^journal/(?P<sid>[0-9]+)/?$','students.views.journal.journal_student', name='journal_student'),
    url(r'^ajax_post/?$','students.views.journal.ajax'),

    # Exams urls
    url(r'^exams/$','students.views.exams.exams_list', name='exams'),
    url(r'^ajax_post_to_exams/?$','students.views.exams.exams_ajax'),

    # Results urls
    url(r'^results/$','students.views.results.results_list', name='results'),

    # AJAX urls
    url(r'^ajax_students_load_more/?$','students.views.homeworks.students_load_more.ajax_load_more', name='ajax_load_more'),
    url(r'^ajax_students_scroll/?$','students.views.homeworks.students_scroll.ajax_scroll', name='ajax_scroll'),

    # Contact
    url(r'^contact-admin/$', 'students.views.contact_admin.contact_admin', name='contact_admin'),
    url(r'', include('contact.urls')),
    
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^myadmin/', admin.site.urls),


]


if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}))
