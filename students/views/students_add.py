# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from students.models.students import Student
from students.models.groups import Group
from django.core.urlresolvers import reverse


def students_add(request):
    # Якщо форма була запощена:
    # was form posted?
    if request.method == "POST":
        # Якщо кнопка Скасувати була натиснута:
        # was form add button clicked?
        if request.POST.get('add_button') is not None:

            # Перевіряємо дані на коректність та збираємо помилки
            # TODO: validate input from user
            errors = {}

            # Якщо дані були введені коректно:
            if not errors:
                # Створюємо та зберігаємо студента в базу
                #create student object
                student = Student(first_name=request.POST['first_name'],
                                  last_name=request.POST['last_name'],
                                  middle_name=request.POST['middle_name'],
                                  birthday=request.POST['birthday'],
                                  ticket=request.POST['ticket'],
                                  student_group=Group.objects.get(pk=request.POST['student_group']),
                                  photo=request.FILES['photo'],)
                student.save()

                # Повертаємо користувача до списку студентів
                # redirect user to students_list
                return HttpResponseRedirect(reverse('home'))
            # Якщо дані були введені некоректно:
            else:
                # Віддаємо шаблон форми разом із знайденими помилками
                # render form with errors and previous user input
                return render(request,'students/forms/students_add.html',
                                      {'groups':Group.objects.all().order_by('title'),
                                       'errors':errors})
        # Якщо форма не була запощена:
        elif request.POST.get('cancel_button') is not None:
            #redirect to home page on cancel button
            print('cancel')
            return HttpResponseRedirect(reverse('home'))
            
    else:
        # initial form render
        # повертаємо код початкового стану форми
        return render(request,'students/forms/students_add.html',
                              {'groups':Group.objects.all().order_by('title')})



