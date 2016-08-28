# -*- coding: utf-8 -*-
from django.shortcuts import render



# Views for Results

def results_list(request): 
    
    return render(request,'students/results_list.html',{})
