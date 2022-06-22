from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ...decorators import *
from ...models import *
from django.db.models import F
from ...filters import SectionFilter, CourseFilter
import csv
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...serializers import *
from datetime import datetime, timedelta, date

@login_required(login_url='/portal/login')
@instructors_only
def list_sections_view(request):
    current_time = datetime.now()

    try:
        current_semester = Semester.objects.get(status=1)
    except Semester.DoesNotExist:
        current_semester = None
    
    if current_semester:
        sections = request.user.instructor.section_set.filter(semester = current_semester)
    else:
        sections = None

    semesters = Semester.objects.filter(registration_starts__range=(request.user.date_joined, current_time))
    context = {
        'sections': sections,
        'semesters': semesters
    }
    return render(request, 'portal/instructor/show_sections.html', context)

def choose_semester_view(request):
    
    return None

@api_view(['GET'])
def list_students_view(request):
    if request.GET.get('json_sec'):
        sid = request.GET['json_sec']
    else:
        return Response({'None': None})

    section = get_object_or_404(Section, pk=sid)
    students = section.students.all().order_by('registration_id')

    serializer = StudentSerializer(students, many=True)

    return Response(serializer.data)

@login_required(login_url='/portal/login')
@instructors_only
def csv_students_list(request, sid):
    # Create the HttpResponse object with the appropriate CSV header.
    section = get_object_or_404(Section, pk=sid)
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="' + str(section) + '.csv"'},
    )

    students_list = section.students.all().order_by('registration_id')

    writer = csv.writer(response)
    writer.writerow([str(section), 'Date: ' + str(datetime.now().strftime("%D %H:%M"))])
    writer.writerow(['Name', 'ID'])

    for student in students_list:
        writer.writerow([student.login.first_name + ' ' + student.login.middle_name + ' ' + student.login.last_name, str(student.registration_id)])

    return response