# -*- coding: utf-8 -*-
from django.shortcuts import render
from students.models.students import Student
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Views for Students Load More

def students_list_load_more(request): 
    students_list = Student.objects.all()

    paginator = Paginator(students_list, 5) # Show 5 students per page

    page = request.POST.get('page')   # listen to AJAX POST from students_load_more.html > load_more.js
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        students = paginator.page(paginator.num_pages)

    paginator_num_pages = paginator.num_pages
    if request.method == 'GET':
        return render(request,'students/homeworks/students_load_more.html',
                              {'students':students,
                               'paginator_num_pages':paginator_num_pages} )
    if request.is_ajax:
        return students


def ajax_load_more(request):
    students = students_list_load_more(request)
    return render(request,'students/homeworks/AJAX_template/ajax_load_more.html', {'students':students})




