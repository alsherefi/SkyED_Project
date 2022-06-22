from django.http import Http404, HttpResponse
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
import json

@login_required(login_url='/portal/login')
@instructors_only
def grade_sections_view(request):
    current_time = datetime.now()

    try:
        # current_semester = Semester.objects.get(exams_ends__lte = current_time, grading_deadline__gte = current_time)
        current_semester = Semester.objects.get(registration_starts__lte = current_time, grading_deadline__gte = current_time)
    except Semester.DoesNotExist:
        return render(request, 'portal/instructor/grading.html', {'not_grade_time': True})

    sections = request.user.instructor.section_set.filter(semester = current_semester)

    # semesters = Semester.objects.filter(registration_starts__range=(request.user.date_joined, current_time))
    context = {
        'sections': sections,
    }

    return render(request, 'portal/instructor/grading.html', context)

@api_view(['GET'])
def list_students_grade_view(request):
    if request.GET.get('json_sec'):
        sid = request.GET['json_sec']
    else:
        return Response({'None': None})

    section = get_object_or_404(Section, pk=sid)
    students = section.studentsection_set.all().order_by('student__registration_id')

    serializer = GradedStudentSerializer(students, many=True)

    return Response(serializer.data)

@login_required(login_url='/portal/login')
@instructors_only
def csv_grades_list(request, sid):
    # Create the HttpResponse object with the appropriate CSV header.
    section = get_object_or_404(Section, pk=sid)
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="' + str(section) + '.csv"'},
    )

    studentsections = section.studentsection_set.all().order_by('student__registration_id')

    writer = csv.writer(response)
    writer.writerow([str(section), 'Date: ' + str(datetime.now().strftime("%D %H:%M"))])
    writer.writerow(['Name', 'ID', 'Grade'])

    for student_section in studentsections:
        writer.writerow([student_section.student.login.first_name + ' ' + student_section.student.login.middle_name + ' ' + student_section.student.login.last_name, str(student_section.student.registration_id), student_section.grade])

    return response

@login_required(login_url='/portal/login')
@instructors_only
@api_view(['POST'])
def ajax_grade_students(request):
    try:
        sid = request.POST.get('json_sec')
        grades = json.loads(request.POST.get('students_grades'))
    except:
        return Response({'error': 'grades and sid bad request'}, status=405)

    students_section = StudentSection.objects.filter(section_id = sid)
    for id, grade in grades.items():
        try:
            student = students_section.get(student__registration_id=id)
        except:
            raise Http404

        if grade != 'n' and student.grade != grade:
            student.grade = grade
            student.save()

    return Response({'succ': 1})