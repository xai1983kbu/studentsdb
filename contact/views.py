from studentsdb.settings import ADMIN_EMAIL

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ContactForm(forms.Form):
    def  __init__(self, *args, **kwargs):
        self.name = forms.CharField(max_length=100,
                                    label="Вашe ім'я")
        self.subject = forms.CharField(max_length=128,
                                       label="Заголовок листа")
        self.email = forms.EmailField(max_length=100,
                                      label=u"Ваша Емейл Адреса")
        self.body = forms.CharField(label=u"Текст повідомлення",
                                    widget=forms.Textarea)

        super(ContactForm, self).__init__(*args, **kwargs)
        # use crispy_forms
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



