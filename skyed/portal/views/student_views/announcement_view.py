from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ...decorators import *
from ...models import *
from django.db.models import F
import datetime
from datetime import datetime, timedelta
from ...filters import SectionFilter, CourseFilter

@login_required(login_url='/portal/login')
@students_only
def announcement_view(request):

    semester = get_object_or_404(Semester, status=1)

    programs = request.user.student.program_set.all()
    departments = programs.values_list('department', flat=True)
    colleges = College.objects.filter(department__in=departments).distinct()
    sections = request.user.student.section_set.filter(semester=semester)

    dept_ann = DeptAnnouncement.objects.filter(department__in=departments, status__in=(1, 2)).annotate(name=F('department__name')).values('name','title', 'info', 'adate')
    college_ann = Announcement.objects.filter(college__in=colleges, status__in=(1, 2)).annotate(name=F('college__college_name')).values('name', 'title', 'info', 'adate')
    section_ann = SectionAnnouncement.objects.filter(section__in=sections, status=1).annotate(name=F('section__course__course_name')).values('name', 'title', 'info', 'adate')

    announcements = dept_ann.union(college_ann).union(section_ann).order_by('-adate')

    context = {
        'announcements': announcements,
    }
    return render(request, 'portal/student/announcement.html', context)
