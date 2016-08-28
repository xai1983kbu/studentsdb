# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from students.models.groups import Group


# Views for Groups
 
def groups_list(request):
    groups = Group.objects.all()

    if request.get_full_path() == "/groups/":
        #redirect request.GET on its copy(deep copy) which I will amend
        request.GET = request.GET.copy()
        #assign 'order_by' value 'last_name' 
        request.GET.__setitem__('order_by', 'title')

    #try to order groups list
    order_by = request.GET.get('order_by', '')

    if request.GET.get('order_by', '') in ('title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse','') == '1':
            groups = groups.reverse()


    paginator = Paginator(groups, 3) # Show 3 contacts per page

    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        groups = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        groups = paginator.page(paginator.num_pages)


    return render(request,'students/groups_list.html',{'groups':groups})



def groups_add(reduest):
    return HttpResponse('<h1>Groups Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)


