from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Group

User = get_user_model()

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
