from django import forms
from studentsdb.settings import ADMIN_EMAIL
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from studentsdb.settings import DEFAULT_FROM_EMAIL, MANAGERS 
from django.contrib import messages
from django.template import loader

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from contact_form.forms import ContactForm
from contact_form.views import ContactFormView

class MyContactFormClass(ContactForm):
    def  __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # use crispy_forms
        self.helper = FormHelper()
        # form tag attributes
        self.helper.form_class = 'form-horisontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_form')
        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        # form buttons
        self.helper.add_input(Submit('send_button', 'Надіслати'))
    # коли дійду до розділу з перекладами name, email та body тут
    # можна буде неперевизначати
    name = forms.CharField(max_length=100,
                           label="Вашe ім'я")
    subject = forms.CharField(max_length=128,
                              required=False,
                              label="Заголовок листа")
    email = forms.EmailField(max_length=100,
                             label=u"Ваша Емейл Адреса")
    body = forms.CharField(label=u"Текст повідомлення",
                           widget=forms.Textarea)
    # вказую порядок полів у формі   
    # field_order насліується з класу BaseForm з яким можна ознайомится
    # за адресою: studentsdb/lib/python3.4/site-packages/django/forms.py
    field_order = ['name', 'subject', 'email', 'body']

    # для відправки листа з html шаблоном
    def message(self):
        # html шаблон для відправки листів
        template_name = 'contact_form/html/contact_form.html'
        return loader.render_to_string(template_name,
                                       self.get_context())

    def save(self, fail_silently=False):
        # self.get_message_dict() дивись в class ContactForm
        # за адресою: studentsdb/lib/python3.4/site-packages/contact-form/forms.py
        message_dict = self.get_message_dict()
        #import pdb; pdb.set_trace();
        send_mail(fail_silently=fail_silently, html_message=message_dict['message'], **self.get_message_dict() )


class MyContactFormView(ContactFormView):
    def  __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def get_success_url(self):
        # This is in a method instead of the success_url attribute
        # because doing it as an attribute would involve a
        # module-level call to reverse(), creating a circular
        # dependency between the URLConf (which imports this module)
        # and this module (which would need to access the URLConf to
        # make the reverse() call).
        list(messages.get_messages(self.request))
        messages.success(self.request,'Повідомлення успішно надіслане!')
        return reverse('contact_form')



    
