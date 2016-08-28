# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from students.models.exams import Exam
from students.models.groups import Group
from students.models.teachers import Teacher
from datetime import datetime
from dateutil.rrule import rrule, MONTHLY, YEARLY
from dateutil.relativedelta import relativedelta
from django.core.urlresolvers import reverse
from django.http import JsonResponse
import json
import ast
from django.conf import settings 
 
# Views for Exams

def exams_list(request): 
    exams = Exam.objects.all().order_by('date_time')        # 'список' усіх екзаменів вітсортованих по даті та часу
    groups = Group.objects.all()                            # 'список' усіх груп
    teachers = Teacher.objects.all()                        # 'список' усіх викладачів                      
    # вормуємо список місяців одного року для меню місяці
    date1 = datetime(2016,1,1)
    date2 = datetime(2016,12,1)
    list_months = list(rrule(MONTHLY, dtstart = date1, until = date2))
    # вормуємо список років для всіх екзаменів
    date3 = exams[0].date_time            # початковий рік так як exams відсортований по 'date_time'
    date4 = exams[len(exams)-1].date_time # кінцевий рік    
    list_years = list(rrule(YEARLY, dtstart = date3, until = date4+relativedelta(years=+1)))  # список років для меню роки
    
    # Сортуємо екзамени або по прізвищу пикладача або по імені викладача
    order_by = request.GET.get('order_by', '')
    if order_by == 'first_name':
        exams = exams.order_by("teaсher__first_name")
    elif order_by == 'last_name':
        exams = exams.order_by("teaсher__last_name")
    
    # Фільтруємо екзамени по вказаному викладачу
    teacher_id=request.GET.get('teacher_id','')
        # Вираз teachers.values_list('id',flat=True) формує список всіх існуючих 'id' в QuerySet 'teachers'
        # list(map(str, ***) перероблює список чисел в список строк
    if teacher_id in list(map(str, teachers.values_list('id',flat=True))):
        exams = exams.filter(teaсher__id = teacher_id)

    # Фільтруємо екзамени по вказаній групі
    group_id=request.GET.get('group_id','')
    if group_id in list(map(str, groups.values_list('id',flat=True))):
        exams = exams.filter(group__id = group_id)  

    # Фільтруємо екзамени по вказаному року
    year_id=request.GET.get('year_id','')
    if year_id:
        exams = exams.filter(date_time__year = year_id)

    # Фільтруємо екзамени по вказаному місяцю
    month_id=request.GET.get('month_id','')
    if month_id:
        exams = exams.filter(date_time__month = month_id)
        print(month_id)
 
    paginator = Paginator(exams, 5) # Show 5 exams per page

    page = request.GET.get('page')
    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        exams = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        exams = paginator.page(paginator.num_pages)

    return render(request,'students/exams_list.html',{'exams':exams,
                                                      'groups':groups,
                                                      'teachers':teachers,
                                                      'list_months':list_months,
                                                      'list_years':list_years})


def exams_ajax(request):
           # menu_teachers:x1, /* дані з меню викладачі */
           # menu_teachers has two values, see <option value="{'order_by':'','filter':''}">
           # menu_groups:x2,   /* дані з меню групи */
           # menu_years:x3,    /* дані з меню роки */
           # menu_months:x4,   /* дані з меню місяці */
           # шаблон url
           # http://127.0.0.1:8000/exams/?order_by=&group_id=&teacher_id=&year=&month=&page=1

    if request.is_ajax():
        if 'menu_teachers' in request.POST:
            menu_teachers = request.POST['menu_teachers']       # Передається ajax запитом з exams_list.html
            menu_teachers=ast.literal_eval(menu_teachers)
            order_by = menu_teachers['order_by']                # Отримуемо необхідний параметр сортування з меню викладачів
            teacher_id = menu_teachers['filter']                # Отримуемо необхідний параметр фільтрування з меню викладачів
        else:
            menu_teachers = False
            order_by = ''
            teacher_id = ''

        if 'menu_groups' in request.POST:
            menu_groups = request.POST['menu_groups']               # Передається ajax запитом з exams_list.html
        else:
            menu_groups = False

        if 'menu_years' in request.POST:
            menu_years = request.POST['menu_years']                   # Передається ajax запитом з exams_list.html
        else:
            menu_years = False

        if 'menu_months' in request.POST:
            menu_months = request.POST['menu_months']                   # Передається ajax запитом з exams_list.html
        else:
            menu_months = False

    # make url kinda http://127.0.0.1:8000/exams/?order_by=&group_id=&teacher_id=&year=&month=&page=1
    url = reverse('exams')
    url = "".join((settings.PORTAL_URL, url, '?order_by=%s'%order_by,'&group_id=%s'%menu_groups,'&teacher_id=%s'%teacher_id,'&year_id=%s'%menu_years,'&month_id=%s'%menu_months,'&page=1'))  

    return JsonResponse({'url':url})
