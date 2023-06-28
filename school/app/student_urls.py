from django.urls import include, path
from .views import Email
from . import views


urlpatterns = [
    path('student-list', views.studentList, name='student-list'),
    path('student-create', views.studentCreate, name='student-create'),
    path('student-update/<int:id>', views.studentUpdate, name='student-update'),
    path('student-delete/<int:id>', views.studentDelete, name='student-delete'),
    path('email/', Email.as_view(), name='send-email'),
]