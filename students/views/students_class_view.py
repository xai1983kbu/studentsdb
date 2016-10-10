# -*- coding: utf-8 -*-
from django.views.generic import ListView
from students.models.students import Student

class StudentList(ListView):
    model = Student
    context_object_name = 'students'
    paginate_by = 5
    paginate_orphans = 5
    page_kwarg = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_logo'] = False
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('last_name')
