from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Group, Student
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import logging
from decouple import config


User = get_user_model()

logger = logging.getLogger(__name__)

HOST = config('MAIL_HOST')
PORT = config('MAIL_PORT')
PASSWORD = config('MAIL_PASSWORD')
USERNAME = config('MAIL_USERNAME')

class UserCreationForm(UserCreationForm):
    phone_number = forms.CharField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    subject_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "phone_number", "group", "subject_name", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.phone_number = self.cleaned_data["phone_number"]
        user.group = self.cleaned_data["group"]
        user.subject_name = self.cleaned_data["subject_name"]
        if commit:
            user.save()
        return user


class EmailForm(forms.Form):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Type message..."
            }
        ),
        label="",
    )

    def send(self):
        msg = MIMEMultipart()

        message = self.cleaned_data["body"]
        msg['From'] = USERNAME

        receivers = []
        for student in Student.objects.all():
            receivers.append(student.email)

        msg['Subject'] = "School"
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(HOST, PORT)
        server.starttls()

        server.login(msg['From'], PASSWORD)
        server.sendmail(msg['From'], receivers, msg.as_string())

        server.quit()
