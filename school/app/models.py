from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class Student(models.Model):
    class Sex(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    name = models.CharField("name", max_length=255)
    last_name = models.CharField("last_name", max_length=255)
    email = models.EmailField("email")
    birth_date = models.DateField("date_of_birth")
    group = models.CharField("class", max_length=127)
    address = models.CharField("address", max_length=255)
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
        print("New student created: {}".format(instance.email))


class Teacher(AbstractUser):
    phone_number = models.CharField("phone_number", max_length=20, default="0", unique=True)
    group = models.CharField("class", max_length=10, default="1-A")
    subject_name = models.CharField("subject_name", max_length=255, default="none")

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.username
