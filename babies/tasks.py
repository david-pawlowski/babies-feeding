import logging
from smtplib import SMTPException
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True)
def send_feeding_mail(self, mail_subject, target_mail, message):
    try:
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[target_mail],
            fail_silently=False,
        )
    except SMTPException:
        logging.error("Email sending failed.")
        return False
    return True
