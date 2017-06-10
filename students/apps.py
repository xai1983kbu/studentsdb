from django.apps import AppConfig


class StudentsConfig(AppConfig):
    name = 'students'
    verbose_name = '---База студентів---'

    def ready(self):
        from students import signals