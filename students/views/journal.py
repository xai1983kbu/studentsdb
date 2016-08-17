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

# Views for Journal
def journal(request, year='2016', month='09'):
    # перехоплення невірних значень year та month 
    try: 
        if int(year) not in range(2000,2051) or int(month) not in range(1,13):
            year = 2016 
            month = 9
    except ValueError:
        year = 2016 
        month = 9 
     
    name_subject=1
    list_subjects = Subject.objects.all()           # Список предметів 
    list_schoolyears = SchoolYear.objects.all()     # Список навчальних років
    schoolyear = SchoolYear.objects.get(title='2016/2017') # Навчальний рік з назвою '2016/2017'
    schoolyear_title = schoolyear.title             # Назва навчального року
    start_year_date = schoolyear.start_year_date    # Дата початку навчального року 
    end_year_date = schoolyear.end_year_date        # Дата закінчення навчального року
    # Список місяців навчального року
    list_months = list(rrule(MONTHLY, dtstart = start_year_date, until = end_year_date))
    # Створюю місяць який відповідає 'year' та 'month'  
    school_month_year = datetime(int(year),int(month),1)  # Треба додати обробник
    # Список календарних днів у вибраному місяці року
    list_days = list(rrule(DAILY, dtstart = school_month_year, until = school_month_year+relativedelta(months=+1, days=-1)))


    #Список лекцій з усіх предметів які відвідав студент з id = 1
    #lectures_all_subject_present_student = Lecture.objects.filter(present_students__id=1) 
    #Список лекції з предмету з title_id = 1 які відвідав студент з id = 1
    #lectures_one_subject_present_student = Lecture.objects.filter(present_students__id=1).filter(title_id=1)
    
    students = Student.objects.all() #список всіх студентів 
    lects_subj_student=[]
    for student in students:
       #список лекцій які відвідує кожен студент з предмету, який має id 'name_subject'
       lects_subj_student.append(Lecture.objects.filter(present_students__id=student.id).filter(title_id=1))#тільки 'Фізика'
  

    return render(request,'students/journal_list.html',{'list_subjects':list_subjects,
                                                        'schoolyear_title':schoolyear_title,
                                                        'school_month_year':school_month_year,
                                                        'list_months':list_months,
                                                        'list_days':list_days,
                                                        'list_schoolyears':list_schoolyears,
                                                        'students':students, 
                                                        'lects_subj_student':lects_subj_student})


def journal_student(request,sid):
    return HttpResponse("<h1>Журнал студента номер %s</h1>"%sid)




