from django.shortcuts import render
from django.http import HttpResponse

# Create your views here

# Views for Students

def students_list(request):
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

    return render(request,'students/students_list.html',{'students':students})

def students_add(reduest):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)


# Views for Groups
 
def groups_list(request):
    groups = (
       {'id': 1,
        'name': '123',
        'leader': 'Волошин Марк'},
       {'id': 2,
        'name': '219',
        'leader': 'Могилевцев Олексій'},
       {'id': 3,
        'name': '203',
        'leader': 'Назаренко Олена'},
)
    return render(request,'students/groups_list.html',{'groups':groups})



def groups_add(reduest):
    return HttpResponse('<h1>Groups Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)

