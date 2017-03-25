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
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        # перевіряємо чи передали нам місяць в параметрі,
        # якщо ні - вичисляємо поточний;
        # поки що ми віддаємо лише поточний:
        today = datetime.today()
        month = date(today.year, today.month, 1)

        # обчислюємо поточний рік, попередній і наступний місяці
        # а поки прибиваємо їх статично:
        context['prev_month'] = '2017-02-01'
        context['next_mont'] = '2017-04-01'
        context['year'] = 2014

        # також поточний місяць;
        # змінну cur_month ми використовуватимо пізніше
        # в пагінації; a month_verbose в
        # навігації помісячній:
        context['cur_month'] = '2017-03-01'
        context['month_verbose'] = 'Липень'

        #
        #
        context['month_header'] = [
            {'day': 1, 'verbose': 'Пн'},
            {'day': 2, 'verbose': 'Вт'},
            {'day': 3, 'verbose': 'Ср'},
            {'day': 4, 'verbose': 'Чт'},
            {'day': 5, 'verbose': 'Пт'}
        ]

        # витягуемо усіх студентів посортованих по
        queryset = Student.objects.order_by('last_name')

        # це адреса посту AJAX запиту, як бачите, ми
        # робитимемо його на цю ж в'юшку; в'юшка журналу
        # буде і показувати журнал і обслуговувати запити
        # типу пост на оновлення журналу;
        update_url = reverse('journal')

        # пробігаємося по усіх студентах і збираємо
        # необхідні дані:
        students = []
        for student in queryset:
            # TODO: витягуємо журнал для студента і
            #       вибраного місяця

            # набиваємо дні для студента
            days = []
            for day in range(1,31):
                days.append({
                    'day': day,
                    'present': True,
                    'date': date(2017, 3, day).strftime(
                        '%Y-%m-%d'),
                })

            # набиваем усі решту даних студента
            students.append({
                'fullname': '%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

            #import pdb;
            #pdb.set_trace();
            # застосовуємо пагінацію по списку студентів
            # context = paginate(students, 10, self.request, context,
            #                   var_name='students')

            # повертаємо оновлений словник із даними
            context['students'] = students

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
