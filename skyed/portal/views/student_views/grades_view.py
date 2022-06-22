from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ...decorators import *
from ...models import *
from django.db.models import F
import datetime
import random
from datetime import datetime, timedelta
from ...filters import SectionFilter, CourseFilter
import qrcode

@login_required(login_url='/portal/login')
@students_only
def grades_view(request, sem):
    if sem == 0:
        studentsections = request.user.student.studentsection_set.filter(section__semester__status=1).order_by('section__start_time')
        if studentsections:
            sem = studentsections[0].section.semester.id
    else:
        studentsections = request.user.student.studentsection_set.filter(section__semester__id=sem).order_by('section__start_time')

    first_semester = request.user.student.semester.registration_starts
    semesters = Semester.objects.filter(registration_starts__gte=first_semester, id__in=(request.user.student.section_set.all().values_list('semester__id', flat=True))).order_by('year', 'semester')

    context = {
        'studentsec': studentsections,
        'semesters': semesters,
        'sem_id': sem,
    }
    return render(request, 'portal/student/grades.html', context)
