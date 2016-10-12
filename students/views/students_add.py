# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from datetime import datetime
from PIL import Image

from students.models.students import Student
from students.models.groups import Group


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
            # import pdb; pdb.set_trace();
            # Перелік дозволених форматів(розширень файлу) для фото
            FORMAT_PHOTO = ('jpg', 'jpeg', 'png', 'bmp') 
            SIZE_PHOTO = 2048*1000 # 2MB - граничний розмір для фото 
            if photo:
                # Користуюся пакетом PIL для відсіювання файлів які не є фото 
                try:
                    im=Image.open(photo) 
                except IOError:
                    errors['photo'] = "Це повино бути фото, наприклад файли з розширеням %s" \
                                    % ", ".join(FORMAT_PHOTO)
                # Перевіряю чи файл з розширенням яке вказано в переліку дозволених
                if photo.content_type.split('/')[1] not in FORMAT_PHOTO: 
                    errors['photo'] = "Фото повино бути одного з цих форматів: %s" \
                                     % ", ".join(FORMAT_PHOTO)
                # Перевіряю чи розмір файл не перевищю дозволеного  
                if photo.size >SIZE_PHOTO:
                    errors['photo'] = "Розмір фото повинен бути менший за 2 мегабайти"
            elif not errors['photo']:
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



