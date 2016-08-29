# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from dateutil.rrule import rrule, MONTHLY, DAILY
from dateutil.relativedelta import relativedelta
from datetime import datetime
from students.models.schoolyears import SchoolYear
from students.models.students import Student
from students.models.lectures import Lecture
from students.models.subjects import Subject
from students.models.groups import Group
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings 

# Views for Journal
def journal(request, year='2014', month='09'):
    # перехоплення невірних значень year та month
    try:
        if int(year) not in range(2000,2051) or int(month) not in range(1,13):
            year = SchoolYear.objects.get(id=1).start_year_date.year
            month = SchoolYear.objects.get(id=1).start_year_date.month
    except ValueError:
        year = SchoolYear.objects.get(id=1).start_year_date.year
        month = SchoolYear.objects.get(id=1).start_year_date.month

    list_subjects = Subject.objects.all()           # Список предметів
    list_schoolyears = SchoolYear.objects.all()     # Список навчальних років
    list_groups = Group.objects.all()               # Список навчальних груп
    year_id=request.GET.get('year','1')             # Зчитую "year_id" з  GET запиту
    schoolyear = SchoolYear.objects.get(id=year_id) # Навчальний рік з id=year_id
    schoolyear_title = schoolyear.title             # Назва навчального року
    start_year_date = schoolyear.start_year_date    # Дата початку навчального року
    end_year_date = schoolyear.end_year_date        # Дата закінчення навчального року
    # Список місяців навчального року
    list_months = list(rrule(MONTHLY, dtstart = start_year_date, until = end_year_date))
    # Створюю місяць який відповідає 'year' та 'month'
    school_month_year = datetime(int(year),int(month),1)  # Дата яка відповідає року "year" та місяцю "month"
    # Список календарних днів у вибраному місяці року
    list_days = list(rrule(DAILY, dtstart = school_month_year, until = school_month_year+relativedelta(months=+1, days=-1)))

    group_id=request.GET.get('group','1')
    students = Student.objects.filter(student_group_id=group_id) #список усіх студентів з групи з id=group_id
    subject_id = request.GET.get('subject','1')
    lects_subj_student=[]
    for student in students:
        #Лекції з предмету з title_id = subject_id на яких був студент  student.id
        lect = Lecture.objects.filter(present_students__id=student.id).filter(title_id=subject_id)
        #список лекцій які відвідує кожен студент з предмету, який має id 'student.id'
        lects_subj_student.append(lect)#тільки 'Фізика'

    return render(request,'students/journal_list.html',{'list_subjects':list_subjects,           # Список предметів
                                                        'schoolyear_title':schoolyear_title,     #
                                                        'school_month_year':school_month_year,
                                                        'list_months':list_months,
                                                        'list_days':list_days,
                                                        'list_schoolyears':list_schoolyears,     # Список навчальних років
                                                        'list_groups':list_groups,               # Список навчальних груп
                                                        'students':students,
                                                        'lects_subj_student':lects_subj_student,
                                                        })

def ajax(request):
    if request.is_ajax():
        if 'schoolyear_id' in request.POST:
            schoolyear_id = request.POST['schoolyear_id']         # Передається ajax запитом з journal_list.html
            schoolyear = SchoolYear.objects.get(id=schoolyear_id) # Навчальний рік з id=schoolyear_id
            start_year_date = schoolyear.start_year_date          # Дата початку навчального року
            year = start_year_date.year                           # Рік початку навчання для навчального року
            month =  start_year_date.month                        # Місяць початку навчання для навчального року
        else:
            schoolyear_id = False

        if 'subject_id' in request.POST:
            subject_id = request.POST['subject_id']               # Передається ajax запитом з journal_list.html
        else:
            subject_id = False

        if 'group_id' in request.POST:
            group_id = request.POST['group_id']               # Передається ajax запитом з journal_list.html
        else:
            group_id = False

    url = reverse('journal_year_month', args=(year,month,))
    url = "".join((settings.PORTAL_URL, url, '/?year=%s'%schoolyear_id,'&subject=%s'%subject_id,'&group=%s'%group_id)) 

    return JsonResponse({'url':url})




def journal_student(request,sid):
    return HttpResponse("<h1>Журнал студента номер %s</h1>"%sid)
