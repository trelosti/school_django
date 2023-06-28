from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import logging
from decouple import config


logger = logging.getLogger(__name__)

HOST = config('MAIL_HOST')
PORT = config('MAIL_PORT')
PASSWORD = config('MAIL_PASSWORD')
USERNAME = config('MAIL_USERNAME')


class Student(models.Model):
    class Sex(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    name = models.CharField("name", max_length=255, null=False)
    last_name = models.CharField("last_name", max_length=255, null=False)
    email = models.EmailField("email", unique=True, null=False)
    birth_date = models.DateField("date_of_birth", null=False)
    group = models.ForeignKey('Group', on_delete=models.PROTECT)
    address = models.CharField("address", max_length=255, null=False)
    sex = models.CharField(
        "sex",
        max_length=1,
        choices=Sex.choices,
        default=Sex.OTHER)

    def __str__(self):
        return "{}".format(self.email)


@receiver(post_save, sender=Student)
def send_student_creation_notification(sender, instance, created, **kwargs):
    if created:
        # logger.warning("New student created: {}".format(instance.email))
        msg = MIMEMultipart()

        message = "Welcome to the school"
        msg['From'] = USERNAME
        msg['To'] = instance.email
        msg['Subject'] = "School"
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(HOST, PORT)
        server.starttls()

        server.login(msg['From'], PASSWORD)
        server.sendmail(msg['From'], msg['To'], msg.as_string())

        server.quit()

class Teacher(AbstractUser):
    phone_number = models.CharField("phone_number", max_length=20, default="0", unique=True)
    group = models.OneToOneField('Group', on_delete=models.PROTECT)
    subject_name = models.CharField("subject_name", max_length=255, default="none")

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.username


class Group(models.Model):
    name = models.CharField("name", max_length=32)
    school = models.ForeignKey('School', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField("name", max_length=32)

    def __str__(self):
        return self.name
