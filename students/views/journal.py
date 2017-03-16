from datetime import date, datetime
from calendar import monthrange, weekday, weekheader
from dateutil.relativedelta import relativedelta

from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from ..models import Student, MonthJournal

class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        context = super(JournalView, self).get_context_data(**kwargs)
        
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d').date()
        else:
            today = datetime.today()
            month = date(today.year, today.month, 1)

        context['month'] = month.strftime('%B')
        context['year'] = month.year

        prev_month = month - relativedelta(months=1)
        next_month = month + relativedelta(months=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')

        days = []
        weekdays = weekheader(2).split(' ')
        for day in range(1, monthrange(month.year, month.month)[1]+1):
            days.append({
                'verbose_name': weekdays[weekday(month.year, month.month, day)],
                'day': day,
            })

        context['days'] = tuple(days)
        
        update_url = reverse('journal')
 
        queryset = Student.objects.all().order_by('last_name')
        
        students = []
        for student in queryset:
            #if student.id == 70:
            #    import pdb; pdb.set_trace()
            
            try:
                journal = MonthJournal.objects.get(student=student, date=month) 
            except:
                journal = None
            
            students.append({
		          'id': student.id,
		          'fullname':'%s %s' % (student.last_name, student.first_name),
		          'update_url': update_url,
		          'days': tuple([{'present': journal and getattr(journal, 'present_day%d' % day) or False,
                                  'date': date(month.year, month.month, day).strftime('%Y-%m-%d') }
                              for day in range(1, monthrange(month.year, month.month)[1]+1) ])
		        },       
		    )
        
        context['students'] = tuple(students)
  
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        
        current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        month = date(current_date.year, current_date.month, 1)
        student = Student.objects.get(pk=data['student_id'])
        present = data['present'] == '1' and True or False
       
        # get and update journal object
        journal = MonthJournal.objects.get_or_create(student=student, date=month)[0]
        setattr(journal, 'present_day%d' % current_date.day, present)
        journal.save()

        return JsonResponse({'status': 'success'})
