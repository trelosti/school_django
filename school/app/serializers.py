
from rest_framework import serializers
from .models import Student
# from .models import Teacher


class StudentSerializer(serializers.ModelSerializer):
  class Meta:
      model = Student
      fields = ['pk', 'name', 'last_name', 'email', 'birth_date', 'group', 'address', 'sex']

# class TeacherSerializer(serializers.ModelSerializer):
#   class Meta:
#       model = Teacher
#       fields = "__all__"