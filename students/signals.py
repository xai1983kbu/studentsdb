import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.termcolors import colorize, parse_color_setting, make_style

from .models import Student, Group, Exam
from django.dispatch import Signal


# setting styles for logging messages
created_green = make_style(opts=('bold',), fg='green')
updated_yellow = make_style(opts=('underscore',), fg='yellow')
delete_red = make_style(opts=('bold',), fg='red')
email_blue = make_style(opts=('bold',), fg='blue')

@receiver(signal = [post_save, post_delete], sender=Student)
@receiver(signal = [post_save, post_delete], sender=Group)
@receiver(signal = [post_save, post_delete], sender=Exam)
def log_student_group_update_added_event(signal, sender, **kwargs):
    """Writes information about newly added or updated student into log file"""
    logger = logging.getLogger(__name__)

    instance = kwargs['instance']

    if signal==post_save:
        # check if instance is a Student and it was created
        if sender==Student and kwargs['created']:
            msg = created_green('Student added: %s %s (ID: %d)'
                                % (instance.first_name, instance.last_name, instance.id))
        # check if instance is a Student and it was updated
        elif sender==Student and not kwargs['created']:
            msg = updated_yellow('Student updated: %s %s (ID: %d)'
                                 % (instance.first_name, instance.last_name, instance.id))
        # check if instance is a Group and it was created
        elif sender==Group and kwargs['created']:
            msg = created_green('Group added: number - %s leader - %s (ID: %d)'
                                % (instance.title, instance.leader, instance.id))
        # check if instance is a Group and it was updated
        elif sender==Group and not kwargs['created']:
            msg = updated_yellow('Group updated: number - %s leader - %s (ID: %d)'
                                 % (instance.title, instance.leader, instance.id))
        # check if instance is an Exam and it was created
        elif sender==Exam and kwargs['created']:
            msg = created_green('Exam added: title - %s date - %s teacher - %s (ID: %d)'
                                % (instance.title, instance.date, instance.teacher, instance.id))
        # check if instance is an Exam and it was updated
        elif sender==Exam and not kwargs['created']:
            msg = updated_yellow('Exam updated: title - %s date - %s teacher - %s (ID: %d)'
                                 % (instance.title, instance.date, instance.teacher, instance.id))
    if signal==post_delete:
        if sender==Student:
            msg = delete_red('Student deleted: %s %s (ID: %d)'
                             % (instance.first_name, instance.last_name, instance.id))
        elif sender==Group:
            msg = delete_red('Group deleted: number - %s leader - %s (ID: %d)' %
                             (instance.title, instance.leader, instance.id))
        elif sender==Exam:
            msg = delete_red('Exam deleted: title - %s date - %s teacher - %s (ID: %d)'
                             % (instance.title, instance.date, instance.teacher, instance.id))

    logger.info(msg)

contact_admin_signal = Signal(providing_args=["subject", "message", "from_email", "admin_email", "excpt"])

@receiver(contact_admin_signal)
def log_contact_admin(**kwargs):
    """Writes information about sending email via contact_email_form"""
    logger = logging.getLogger(__name__)
    msg = email_blue('sender - %s subject - %s message - %s from_email - %s admin_email - %s exception - %s'
                     % (kwargs['sender'], kwargs['subject'], kwargs['message'], kwargs['from_email'], \
                        kwargs['admin_email'], kwargs['excpt']))
    logger.info(msg)