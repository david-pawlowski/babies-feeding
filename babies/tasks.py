import logging
import http.client
import urllib

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


@shared_task(bind=True)
def send_push_notification(self, message, target_token):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request(
        "POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": settings.PUSHOVER_API_TOKEN,
            "user": target_token,
            "message": message,
        }),
        {"Content-type": "application/x-www-form-urlencoded"}
    )
    conn.getresponse()
