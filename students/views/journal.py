from django.shortcuts import render
from django.http import HttpResponse

# Views for Journal
def journal(request):
    students = (
        {'id': 1,
         'first_name': 'Андрій',
         'last_name': 'Сорочан',
         'ticket': 2123,
         'image': 'img/my_photo.jpg'},
        {'id': 2,
         'first_name': 'Андрій2',
         'last_name': 'Сорочан2',
         'ticket': 21232,
         'image': 'img/my_photo2.jpg'},
        {'id': 3,
         'first_name': 'Андрій3',
         'last_name': 'Сорочан3',
         'ticket': 21233,
         'image': 'img/my_photo3.jpg'},
)
    return render(request,'students/journal_list.html',{'students':students})

def journal_student(request,sid):
    return HttpResponse("<h1>Журнал студента номер %s</h1>"%sid)
