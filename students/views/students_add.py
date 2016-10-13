# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
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

            photo = request.FILES.get('photo') # об*єкт класу InMemoryUploadedFile
            FORMAT_PHOTO = ('jpg', 'jpeg', 'png', 'bmp') 
            SIZE_PHOTO = 10 # 10MB - граничний розмір для фото
            SIZE_THUMNAIL = (500, 500)
            # Перевіряю на допустимий розмір файла
            if photo.size >SIZE_PHOTO*1024*1000:
                errors['photo'] = "".join(["Розмір фото не повинен перевищувати ", str(SIZE_PHOTO), " мегабайт"])
                photo = None
            if photo:
                # Користуюся пакетом PIL для відсіювання файлів які не є фото 
                try:          
                    img = Image.open(photo)
                    img.thumbnail(SIZE_THUMNAIL, Image.ANTIALIAS)
                    thumb_io = BytesIO()
                    _format = photo.content_type.split('/')[1]
                    img.save(thumb_io, _format)
                    # Ініціалізатор для InMemoryUploadedFile, дивись 
                    # /data/work/virtualenv3/studentsdb/lib/python3.4/site-packages/django/core/files/uploadedfile.py
                    # __init__(self, file, field_name, name, content_type, size, charset, content_type_extra=None):
                    _file = thumb_io
                    field_name = photo.field_name
                    name = "".join([datetime.now().strftime("%Y-%m-%d %H-%M-%S"),".", _format])
                    content_type = photo.content_type
                    im = InMemoryUploadedFile(_file, field_name, name, content_type, size=None, charset=None)
                    data['photo'] = im
                    #qimport pdb; pdb.set_trace();
                except IOError:
                    errors['photo'] = "Це повино бути фото, наприклад файли з розширеням %s" \
                                    % ", ".join(FORMAT_PHOTO)
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



