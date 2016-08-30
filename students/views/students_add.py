# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from students.models.students import Student
from students.models.groups import Group
from django.core.urlresolvers import reverse
from datetime import datetime

def students_add(request):
    # Якщо форма була запощена:
    # was form posted?
    if request.method == "POST":
        # Якщо кнопка Додати була натиснута:
        # was form add button clicked?
        if request.POST.get('add_button') is not None:
            data = {'middle_name':request.POST['middle_name'], 
                    'notes': request.POST['notes']}
            # Перевіряємо дані на коректність та збираємо помилки
            # validate input from user
            errors = {}

            first_name = request.POST.get('first_name','').strip()
            if not first_name:
                errors['first_name'] = "Ім'я є обов'язковим"
            else: 
                data['first_name'] = first_name

            last_name = request.POST.get('last_name','').strip()
            if not last_name:
                errors['last_name'] = "Прізвище є обов'язковим"
            else: 
                data['last_name'] = last_name

            ticket = request.POST.get('ticket','').strip()
            if not ticket:
                errors['ticket'] = "Квиток є обов'язковим"
            else: 
                data['ticket'] = ticket

            birthday = request.POST.get('birthday','').strip()
            if not birthday:
                errors['birthday'] = "Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday,'%Y-%m-%d')
                except Exception:
                    errors['birthday'] = \
                        "Введіть коректний формат дати (напр. 1984-12-30)"
                else:
                    data['birthday'] = birthday

            student_group = request.POST['student_group']
            if not student_group:
                errors['student_group'] = "Група є обов'язковою"
            else: 
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = "Оберіть коректну групу" 
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo 

            #зберігаємо студента
            # Якщо дані були введені коректно:
            if not errors:
                # Створюємо та зберігаємо студента в базу
                #create student object
                student = Student(**data)
                student.save()
                # Повертаємо користувача до списку студентів
                # redirect user to students_list
                return HttpResponseRedirect('%s?status_message=Студента успішно додано!' %
reverse('home'))
            # Якщо дані були введені некоректно:
            else:
                # Віддаємо шаблон форми разом із знайденими помилками
                # render form with errors and previous user input
                return render(request,'students/forms/students_add.html',
                                      {'groups':Group.objects.all().order_by('title'),
                                       'errors':errors})
        # Якщо кнопка Скасувати була натиснута:
        elif request.POST.get('cancel_button') is not None:
            #Повертаємо користувача до списку студентів
            #redirect to home page on cancel button
            return HttpResponseRedirect('%s?status_message=Додавання студента скасовано!' %
reverse('home'))
    # Якщо форма не була запощена:       
    else:
        # initial form render
        # повертаємо код початкового стану форми
        return render(request,'students/forms/students_add.html',
                              {'groups':Group.objects.all().order_by('title')})



