# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Student

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


def students_add(reduest):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)

