# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

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


