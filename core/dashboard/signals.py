# import dispacher, receiver, and post_save
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import string
import random

from accounts.models import User, OTP
import core.settings as settings

# globals
email_template = 'dashboard/notifications/password_otp_template.html'


@receiver(post_save, sender=User)
def mail_user_password(sender, instance, created, **kwargs):
    '''sends the user password to the user's email'''
    if created:
        passcode = generate_user_password()
        if instance.created_from_dashboard:
            subject = 'New Account Setup'
            message = 'Hello there, your account[for dlcf app] has been created. \nUse the password below to login to your account'  # noqa
            receipients = [str(instance.email)]
            send_email(instance, email_template, passcode, subject, message, receipients)  # noqa
            instance.set_password(passcode)
            instance.save()


@receiver(post_save, sender=OTP)
def mail_user_otp(sender, instance, created, **kwargs):
    '''sends the user otp to the user's email'''
    if created:
        passcode = instance.otp
        subject = 'One Time Password'
        message = 'Hello there, your one time password is: '
        receipients = [instance.user.email]
        try:
            send_email(instance, email_template, passcode,
                       subject, message, receipients)
        except Exception as e:
            print(e)
        else:
            print('OTP sent to: ', receipients, 'OTP CODE: ', passcode)
        finally:
            print("The mail_user_opt function has been called")


@receiver(post_save, sender=User)
def mail_user_password(sender, instance, created, **kwargs):
    '''sends the user password to the user's email'''
    if created:
        if instance.created_from_dashboard:
            subject = 'New Account Setup'
            message = 'Hello there, your account[for dlcf app] has been created. \nUse the password below to login to your account'
            receipients = [str(instance.email)]
            passcode = generate_user_password()
            instance.set_password(passcode)
            instance.save()
            send_email(instance, email_template, passcode,
                       subject, message, receipients)


def send_email(instance, template_name: str, password: str, subject: str, message, receipients):  # noqa
    '''Send mail to user who booked the trip'''
    text = render_to_string(template_name, {
        'instance': instance,
        'passcode': password,
        'message': message,
        'subject': subject,
    })
    msg = EmailMultiAlternatives(
        subject.upper(), text,
        settings.EMAIL_HOST_USER, receipients)
    msg.attach_alternative(text, "text/html")
    try:
        msg.send()
    except Exception as err:
        print(err)
    else:
        print("Successful....Email sent to: ", receipients)


def generate_user_password():
    '''generate a random password for the user'''
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    size = 8
    return ''.join(random.choice(chars) for _ in range(size))


def generate_otp():
    '''generate a random otp for the user'''
    chars = string.digits
    size = 4
    return ''.join(random.choice(chars) for _ in range(size))
