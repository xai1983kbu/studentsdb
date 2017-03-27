

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from ..models import MonthJournal, Student
# from ..util import paginate


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        # check if we need to display some specific month
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d'
                                      ).date()
        else:
            # otherwise just displaying current data
            today = datetime.today()
            month = date(today.year, today.month, 1)


        # calculate current, previous and next month details;
        # we need this for month navigation element in template
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')

        # we'll use this variable in students pagination
        context['cur_month'] = month.strftime('%Y-%m-%d')

        # prepare variable for template to generate
        # journal table header elements
        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [{'day': d,
                                    'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
                                    for d in range(1, number_of_days+1)]

        # get all students from database
        queryset = Student.objects.order_by('last_name')

        # url to update student presence, for rorm post
        update_url = reverse('journal')

        # go over all students and collect data about presence
        # during selected month
        students = []
        for student in queryset:
            # try to get journal object by month selected
            # month and current student
            try:
                journal = MonthJournal.objects.get(student=student, date=month)
            except Exception:
                journal = None


            # fill in days presence list for current student
            days = []
            for day in range(1, number_of_days+1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day%d' %
                                                   day, False) or False,
                    'date': date(myear, mmonth, day).strftime(
                        '%Y-%m-%d'),
                })

            # prepare metadata for current student
            students.append({
                'fullname': '%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

        context['students'] = students


        # import pdb
        # pdb.set_trace()
        # apply pagination, 10 students per page
        # context = paginate(students, 10, self.request, context,
        #                   var_name='students')

        # finnally return update context
        # with paginated students
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
