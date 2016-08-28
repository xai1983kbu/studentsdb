# -*- coding: utf-8 -*-

from django.db import models

class Exam(models.Model):
    """Exam Model"""

    class Meta(object):
        verbose_name = "Екзамен"
        verbose_name_plural = "Екзамени" 

    title = models.ForeignKey('Subject',
        verbose_name=u"Предмет з якого проводитиметься екзамен",
        blank=False)

    date_time = models.DateTimeField(
        verbose_name = "Дата та час проведеня екзамену",
        blank = False)

    teaсher = models.ForeignKey('Teacher',
        verbose_name=u"Викладач",
        blank=False)

    group = models.ForeignKey('Group',
        verbose_name=u"Група для якої проводитиметься екзамен",
        blank=False)
    

    def  __str__(self):
        return "%s %s" % (self.title, self.date_time)
