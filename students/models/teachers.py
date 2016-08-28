# -*- coding: utf-8 -*-

from django.db import models

class Teacher(models.Model):
    """Teacher Model"""

    class Meta(object):
        verbose_name = "Викладач"
        verbose_name_plural = "Викладачі" 


    first_name = models.CharField(
        max_length = 256,
        blank = False,
        verbose_name = "Ім'я")


    last_name = models.CharField(
        max_length = 256,
        blank = False,
        verbose_name = "Прізвище")


    middle_name = models.CharField(
        max_length = 256,
        blank = True,
        verbose_name = "По-батькові",
        default = '')


    salary = models.IntegerField(
        verbose_name = "Середня зарабітня платня за останній рік")


    def  __str__(self):
        return "%s %s" % (self.last_name, self.first_name)
