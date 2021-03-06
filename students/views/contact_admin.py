# -*- coding: utf-8 -*-
from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from studentsdb.settings import ADMIN_EMAIL
from django.contrib import messages
import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from ..signals import contact_admin_signal


class ContactForm(forms.Form):
    def  __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        # form tag attributes
        self.helper.form_class = 'form-horisontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.add_input(Submit('send_button', 'Надіслати'))

    from_email = forms.EmailField(
        label=u"Ваша Емейл Адреса")

    subject = forms.CharField(
        label=u"Заголовок листа",
        max_length=128)

    message = forms.CharField(
        label=u"Текст повідомлення",
        widget=forms.Textarea)

def contact_admin(request):
    # check if form was posted
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)

        # check whether user data is valid:
        if form.is_valid():
            # send email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            try:
                send_mail(subject, message, from_email, [ADMIN_EMAIL])
                contact_admin_signal.send(sender=ContactForm, subject=subject, message=message, from_email=from_email,\
                                          admin_email=[ADMIN_EMAIL], excpt=None)
            except Exception as e:
                contact_admin_signal.send(sender=ContactForm, subject=subject, message=message, from_email=from_email,\
                                          admin_email=[ADMIN_EMAIL], excpt=e)
                message = 'Під час відправки листа виникла непередбачувана помилка.' \
                          'Спробуйте скористатись даною формою пізніше.'
                messages.warning(request, message)
            else:
                messages.warning(request,'Попереднє непотрідне повідомлення')
                list(messages.get_messages(request))
                #import pdb; pdb.set_trace();
                messages.success(request,'Повідомлення успішно надіслане!')
            # redirect to same contact page with success message
            return HttpResponseRedirect(reverse('contact_admin'))

    # if there was not POST render blank form
    else:
        form = ContactForm()

    return render(request, 'contact_admin/form.html', {'form': form})
