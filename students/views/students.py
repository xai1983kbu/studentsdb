# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.forms import ModelForm
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models import Student, Group
from ..util import paginate


class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # set form tag attributes
        self.helper.form_action = reverse('students_edit',
            kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        # add buttons
        self.helper.layout.fields.append(FormActions(
            Submit('add_button', 'Зберегти', css_class='btn btn-primary'),
            Submit('cancel_button', 'Скасувати', css_class='btn btn-link'),)
        )


class StudentUpdateView(UpdateView):
    model = Student
    #fields = '__all__'
    template_name_suffix = '_edit'
    form_class = StudentUpdateForm
    #template_name = 'students/student_edit.html'
    success_url = 'home'
    success_message = 'Студента {} успішно збережено!'
    cancel_message = 'Редагування студента {} відмінено!'   
    def get_success_url(self):
        student = self.model.objects.filter(id=self.kwargs['pk'])
        if student:
            student = student.get()
        list(messages.get_messages(self.request))
        messages.success(self.request, self.success_message.format(student))
        #import pdb; pdb.set_trace()
        return reverse(self.success_url)

    def post(self, request, *args, **kwargs):
        #import pdb; pdb.set_trace()
        student = self.model.objects.filter(id=self.kwargs['pk'])
        if student:
            student = student.get()
        if request.POST.get('cancel_button'):
            list(messages.get_messages(self.request))
            messages.warning(self.request, self.cancel_message.format(student))
            return HttpResponseRedirect(reverse(self.success_url))
        else:
            return super().post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    success_url = 'home'
    template_name_suffix = '_confirm_delete'
    success_message = "Студента %s успішно видалено!"

    #http://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message \
                         % self.model.objects.filter(pk=kwargs['pk'])[0].__str__())
        #import pdb; pdb.set_trace()
        return super(StudentDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(self.success_url)


class ManyStudentDeleteView(DeleteView):
    model = Student
    success_url = 'students_scroll'
    template_name_suffix = '_confirm_many_delete'
    success_message = "Студента %s успішно видалено!"
    context_object_name = 'list_objects_of_model'
    success_message = 'Студентів успішно видалено!'
    cancel_message = 'Видалення студентів відмінено!'

    def get_queryset(self):
        qs = super().get_queryset()
        list_id_of_students = self.request.GET.getlist('delete_list')
        #import pdb; pdb.set_trace();
        return qs.filter(id__in=list_id_of_students)

    # перевизначаю 'get_object' з /lib/python3.4/site-packages/django/views/generic/detail.py
    # щоб не було помилки 'must be called with either an object -pk or a slug'
    # obj передається в 'student_confirm_many_delete.html' під псевдонімом 'list_objects_of_model'
    def get_object(self, queryset=None):
        obj = self.get_queryset()
        return obj

    def delete(self, request, *args, **kwargs):
        if self.request.POST.get('delete_button') is not None:
            list_id_of_students = request.POST.getlist('delete_list')
            self.model.objects.filter(id__in=list_id_of_students).delete()
        success_url = self.get_success_url()
        #import pdb; pdb.set_trace();
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        #import pdb; pdb.set_trace()
        list(messages.get_messages(self.request))
        if self.request.POST.get('cancel_button') is not None:
            messages.warning(self.request, self.cancel_message)
        if self.request.POST.get('delete_button') is not None:
            messages.success(self.request, self.success_message) 
        return reverse(self.success_url)


# Views for Students
class StudentView(TemplateView):
    template_name = "students/students_list.html"

    def get_context_data(self, **kwargs):
        # get context data from TempaleView class
        context = super(StudentView, self).get_context_data(**kwargs)
        students = Student.objects.all()

        if self.request.GET.get('order_by', '') in ('first_name', 'last_name'):
            students = students.order_by(self.request.GET.get('order_by', ''))
        elif self.request.GET.get('order_by', '') in ('ticket'):
            students = Student.objects.extra(
                select={'ticket': 'CAST(ticket AS SIGNED)'}
                ).order_by('ticket')

        if self.request.GET.get('reverse', '') == '1':
            students = students.reverse()

        context = paginate(students, 10, self.request, context,
                           var_name='students')
        #import pdb; pdb.set_trace();
        return context

    def get(self, request, *args, **kwargs):

        if request.get_full_path() == "/":
            # redirect request.GET on its copy(deep copy) which I will amend
            request.GET = request.GET.copy()
            # assign 'order_by' value 'last_name'
            request.GET.__setitem__('order_by', 'last_name')
            # assign 'page' value '1'
            request.GET.__setitem__('page', '1')

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

