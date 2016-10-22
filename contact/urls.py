
from django.conf.urls import url
from django.views.generic import TemplateView

from contact.forms import MyContactFormView

from contact.forms import MyContactFormClass

urlpatterns = [
    # ... other URL patterns for your site ...
    url(r'^contact/$',
        MyContactFormView.as_view(
            form_class=MyContactFormClass),
            name='contact_form')
]
