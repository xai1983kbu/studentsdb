# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError

class Group(models.Model):
    """Group Model"""

    class Meta(object):
        verbose_name = "Група"
        verbose_name_plural = "Групи"

    title = models.CharField(
        max_length = 256,
        blank = False,
        verbose_name = "Назва")

    leader = models.OneToOneField('Student',
        verbose_name = u"Староста",
        blank = True,
        null = True,
        on_delete = models.SET_NULL)

    notes = models.TextField(
        blank = True,
        verbose_name = "Додаткові нотатки")

    def clean(self):
        if self.title is not None:
            group = Group.objects.filter(title = self.title)
            if self.leader is not None and self.leader.student_group not in group:
                raise ValidationError({'leader': 'Цей студент не з цієї групи! '
                          'Обрати можна тільки студента з групи %s' % self.title}
                      )
        #import pdb; pdb.set_trace()

    
    def __str__(self):
        if self.leader:
            return "%s  (%s,%s)" % (self.title, self.leader.first_name, self.leader.last_name)
        else:
            return "%s" % (self.title,)
