from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .forms import UserCreationForm
from .models import Student
from rest_framework import generics
from .serializers import StudentSerializer


@method_decorator(login_required, name='dispatch')
class StudentCreate(generics.CreateAPIView):
    model = Student
    queryset = Student.objects.all(),
    serializer_class = StudentSerializer


@method_decorator(login_required, name='dispatch')
class StudentList(generics.ListAPIView):
    model = Student
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

@method_decorator(login_required, name='dispatch')
class StudentDetail(generics.RetrieveAPIView):
    model = Student
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

@method_decorator(login_required, name='dispatch')
class StudentUpdate(generics.RetrieveUpdateAPIView):
    model = Student
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

@method_decorator(login_required, name='dispatch')
class StudentDelete(generics.RetrieveDestroyAPIView):
    model = Student
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password1')
            user = authenticate(phone_number=phone_number, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }

        return render(request, self.template_name, context)