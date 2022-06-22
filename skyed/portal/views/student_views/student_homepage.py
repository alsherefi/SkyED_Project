from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ...decorators import *
from ...models import *
from django.db.models import F
import datetime
from datetime import datetime, timedelta
from ...filters import SectionFilter, CourseFilter

def get_registration_semester(current_time=datetime.now(), weeks=timedelta()):
    try:
        semester = Semester.objects.get(registration_starts__lte=current_time+weeks, registration_ends__gte=current_time)
    except Semester.DoesNotExist:
        semester = None

    return semester

# student_homepage
# Returns:-
# announcements(Queryset): Group of announcements from sections, departments and colleges.
#   You can loop on it. for ann in announcements: ann.name(sender), ann.title, ann.adate, ann.info
# register_soon(Boolean): True if the registration is after two weeks.
# register_time(Boolean): True if it's registration period
# graded: Returns graded courses if any
# semester: Returns the registration semester.
# Student: request.user.student

@login_required(login_url='/portal/login')
@students_only
def student_homepage(request):
    current_time = datetime.now()
    weeks = timedelta(days=14)
    month = timedelta(days=30)
    semester = get_registration_semester(current_time, timedelta(days=-14))

    programs = request.user.student.program_set.all()
    departments = programs.values_list('department', flat=True)
    colleges = College.objects.filter(department__in=departments).distinct()
    sections = request.user.student.section_set.filter(semester=semester)

    dept_ann = DeptAnnouncement.objects.filter(department__in=departments, status__in=(1, 2)).annotate(name=F('department__name')).values('name','title', 'info', 'adate')
    college_ann = Announcement.objects.filter(college__in=colleges, status__in=(1, 2)).annotate(name=F('college__college_name')).values('name', 'title', 'info', 'adate')
    section_ann = SectionAnnouncement.objects.filter(section__in=sections, status=1).annotate(name=F('section__course__course_name')).values('name', 'title', 'info', 'adate')

    announcements = dept_ann.union(college_ann).union(section_ann).order_by('-adate')

    register_time = False
    register_soon = False

    if semester:
        if semester.registration_starts <= current_time <= semester.registration_ends:
            register_time = True
        elif  current_time < semester.registration_starts <= current_time + weeks:
            register_soon = True
        else:
            print(current_time - weeks, semester.registration_starts, current_time, sep='\n')

    graded = None
    try:
        previous_semester = Semester.objects.get(semester_starts__lte=current_time+month, semester_ends__gte=current_time+month)
        graded = request.user.student.studentsection_set.filter(section__semester=previous_semester, grade__isnull=False)
    except:
        previous_semester = None

    credits_percentage = round(request.user.student.credits / 129 * 100)
    major_credits_percentage = round(request.user.student.major_credits / 60 * 100)

    context = {
        'announcements': announcements,
        'register_time': register_time,
        'register_soon': register_soon,
        'graded': graded,
        'semester': semester,
        'student': request.user.student,
        'credits_percentage': credits_percentage,
        'major_credits_percentage': major_credits_percentage,
    }
    return render(request, 'portal/student/student_homepage.html', context)
