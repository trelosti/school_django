from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from .forms import UserCreationForm, EmailForm, StudentForm
from .models import Student


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


class Email(View):
    template_name = 'email.html'

    def get(self, request):
        context = {
            'form': EmailForm()
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = EmailForm(request.POST)

        if form.is_valid():
            form.send()
            return redirect('home')
        context = {
            'form': form
        }

        return render(request, self.template_name, context)


@login_required()
# Create your views here.
def studentList(request):
    students = Student.objects.all()
    return render(request, "student-list.html", {'students': students})


@login_required()
def studentCreate(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('student-list')
            except:
                pass
    else:
        form = StudentForm()
    return render(request, 'student-create.html', {'form': form})


@login_required()
def studentUpdate(request, id):
    student = Student.objects.get(id=id)
    form = StudentForm(
        initial={'name': student.name, 'last_name': student.last_name,
                 'email': student.email, 'birth_date': student.birth_date,
                 'group': student.group, 'address': student.address, 'sex': student.sex})

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('student-list')
            except Exception as e:
                pass
    return render(request, 'student-update.html', {'form': form})


@login_required()
def studentDelete(request, id):
    student = Student.objects.get(id=id)
    try:
        student.delete()
    except:
        pass
    return redirect('student-list')
