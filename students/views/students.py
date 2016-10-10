# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.forms import ModelForm
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models import Student, Group


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
        self.helper.layout[-1] = FormActions(
            Submit('add_button', 'Зберегти', css_class='btn btn-primary'),
            Submit('cancel_button', 'Скасувати', css_class='btn btn-link'),)


class StudentUpdateView(UpdateView):
    model = Student
    #fields = '__all__'
    template_name_suffix = '_edit'
    form_class = StudentUpdateForm
    #template_name = 'students/student_edit.html'
   
    def get_success_url(self):
        return '%s?status_message=Студента успішно збережено' \
            % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                '%s?status_message=Редагування студента відмінено' \
                % reverse('home'))
        else:
            return super().post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    success_url = 'home'
    template_name_suffix = '_confirm_delete'
    status_message = 'Студента успішно видалено!'

    def get_success_url(self):
        return '%s?status_message=%s' % (reverse(self.success_url), self.status_message)


# Views for Students
def students_list(request): 
    students = Student.objects.all()

    if request.get_full_path() == "/":
        #redirect request.GET on its copy(deep copy) which I will amend
        request.GET = request.GET.copy()
        #assign 'order_by' value 'last_name' 
        request.GET.__setitem__('order_by', 'last_name')
        #assign 'cadre' value '1' 
        request.GET.__setitem__('cadre', '1')
        request.GET.__setitem__('page', '1')
 
    #try to order students list
    order_by = request.GET.get('order_by', '')

    if request.GET.get('order_by', '') in ('first_name', 'last_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse','') == '1':
            students = students.reverse()
 
   
    #paginate students
    num_students_in_one_page = 3
    num_pages_in_on_cadre = 2
    num_students_in_one_cadre = num_students_in_one_page * num_pages_in_on_cadre

    paginator_inner  = Paginator(students, num_students_in_one_cadre)   # Students divided up cadre
    page = request.GET.get('page')
    cadre = request.GET.get('cadre')

    try:
        cadres_set = paginator_inner.page(cadre)                        # Cadre number='cadre' 
        paginator = Paginator(cadres_set, num_students_in_one_page)     # Set of pages of students, show 3 students per page 
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page and cadre  are not an integer, deliver first page.
        cadre = 1
        cadres_set = paginator_inner.page(cadre)                        # First cadre
        # Set of pages of students for first cadre, show 3 students per page
        paginator = Paginator(cadres_set, num_students_in_one_page)       
        students = paginator.page(1)                                    #first page of students from first cadre
    except EmptyPage:
        # If page and cadre are  out of range (e.g. 9999), deliver last page of results.
        cadre = paginator_inner.num_pages
        cadres_set = paginator_inner.page(cadre)
        paginator = Paginator(paginator_inner.page(paginator_inner.num_pages), num_students_in_one_page) #last cadre
        students = paginator.page(paginator.num_pages)                   #last student from last cadre

    #Do range of numeration of pages in each cadre
    page_start_index = 2*(int(cadre)-1)+1
    page_end_index = 2*(int(cadre)-1)+students.paginator.num_pages
    page_range_in_cadre = range(1,students.paginator.num_pages+1)      # Range of pages numbers only for one cadre
    page_range_in_document = range(page_start_index,page_end_index+1)  # Range of pages numbers for whole document
    combined_page_rage = [{'num_in_cadre':i,'num_in_document':k} for i,k in zip(page_range_in_cadre,page_range_in_document)] 
    return render(request,'students/students_list.html',{'students':students, 'cadres_set':cadres_set,
                          'combined_page_rage':combined_page_rage})




