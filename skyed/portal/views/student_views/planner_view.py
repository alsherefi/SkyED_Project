from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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
from .student_homepage import get_registration_semester
from ...forms import CourseForm
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...serializers import CourseSerializer
from django.urls import reverse

# Note: The main function is the planner_view

def get_sem_number(semester):
	if semester == "Fall":
		return 1
	elif semester == "Spring":
		return 2
	elif semester == "Summer":
		return 3
	else:
		return -1

def get_semester(semester, year):
	try:
		semester = Semester.objects.get(year=year, semester=semester)
	except Semester.DoesNotExist:
		semester = None

	return semester

def get_current_semester():
	current_time = datetime.now()
	try:
			semester = Semester.objects.get(semester_starts__lte=current_time, semester_ends__gte=current_time)
	except Semester.DoesNotExist:
			semester = None

	return semester

# get_planner_semesters
# Returns:-
# semesters(list(string, integer)): a list tuples (semesester, year) from the student's first_year to five years ahead.
def get_planner_semesters(first_semester, first_year):
	y = first_year
	if first_semester == 1:
		semesters = [('Fall', y, y+1), ]
	else:
		semesters = []

	semesters.append(('Spring', y, y+1))
	semesters.append(('Summer', y, y+1))

	for i in range(1, 5):
		y = first_year + i
		semesters.append(('Fall', y, y+1))
		semesters.append(('Spring', y, y+1))
		semesters.append(('Summer', y, y+1))
	
	return semesters


# check_requisites: This function checks whether a chosen course has a prequisites that are not in the planner yet.
# Parameters:-
# student(class Student): Student object from the models class Student.
# course(string): course id
# semester(string): the chosen semester in the planner
# year(int): the chosen year in the planner
# Returns
# not_passed(list[(string, string)]): a list of tuples(course_id, course_name) that returns all of the courses that the student didn't pass if the subject he wanted to add had a prerequisite.
def check_requisites(student, course, semester, year):
	s = [get_sem_number(semester)]
	print('course:', course)
	print('semester:', semester)
	print('year:', year)

	if semester == 'Fall':
		s.append(2)
		s.append(3)
	elif semester == 'Spring':
		s.append(3)

	course = get_object_or_404(Course, pk=course)
	print('Course Model:', course)

	requisites = course.requisites.filter(requisite__requisite_type='prerequisite').values_list('course_id', 'course_name')
	planner = student.studentcourseplan_set.filter(year__lte=year).exclude(year=year, semester__in=s).values_list('course__course_id', 'course__course_name')
	not_passed = []

	for requisite in requisites:
		if requisite not in planner:
			not_passed.append((requisite))

	return not_passed

# planner_view:
# returns:-
# student_courses(class Course): the courses from the plan table in a specfic semester. It can be None. You can loop on it.
# first_year(integer): The student's first year in the university
# first_semester(string): The student's first semester in the University
# semesters(list(string, integer)): a list tuples (semesester, year) from the student's first_year to five years ahead.
# courses(class Course): the result search of the courses. You can loop on it.
# form: the form for searching the courses
# added_to_plan(Boolean): returns True if the course was added successfully
# not_passed(list[(string, string)]): a list of tuples(course_id, course_name) that returns all of the courses that the student didn't pass if the subject he wanted to add had a prerequisite.
# 	Example: A student wanted to add Programming in C to his plan but he didn't put Programming 1 yet.
 
@login_required(login_url='/portal/login')
@students_only
def planner_view(request):
	selected_semester = None
	s1 = request.session.get('semester')
	not_passed = request.session.get('not_passed') # not_passed for the courses the student didn't pass if he wanted to add.
	added_to_plan = request.session.get('added_to_plan') # if the course was added successfully
	result = None # a variable that stores the semester from the form (method GET)
	isnew = True

	departments = Department.objects.all()

	if not_passed:
		del(request.session['not_passed'])
	if added_to_plan:
		del(request.session['added_to_plan'])

	if 'semester' in request.GET:
		result = request.GET['semester']
		result = result.split()
		print('semester = ',result)
	if s1:
		result = s1
		del(request.session['semester'])

	# Gets the semester that the student chose
	if result:
		try:
			selected_semester = (result[0], int(result[1]), int(result[2]))
		except:
			return redirect(reverse('portal:planner_view'))

		rsemester = get_sem_number(result[0])
		ryear = result[1]
		semester = get_semester(rsemester, ryear) # returns the chosen semester

		if semester and semester.semester_ends < datetime.now().date():
			isnew = False

		student_courses = request.user.student.course_set.filter(studentcourseplan__semester=rsemester, studentcourseplan__year=ryear)

	else:
		semester = get_registration_semester()
		if semester == None:
			semester = get_current_semester()
		
		if semester and semester.semester_ends < datetime.now().date():
			isnew = False

		selected_semester = (semester.get_semester_display(), semester.year, semester.year+1)
		student_courses = request.user.student.course_set.filter(studentcourseplan__semester=semester.semester, studentcourseplan__year=semester.year)

	first_semester = request.user.student.semester

	semesters = get_planner_semesters(first_semester.semester, first_semester.year)
	
	context = {
		'student_courses': student_courses,
		'first_year': None,
		'semesters': semesters,
		'selected_semester': selected_semester,
		'added_to_plan': added_to_plan,
		'not_passed': not_passed,
		'departments': departments,
		'isnew': isnew,
	}
	return render(request, 'portal/student/zplanner.html', context)

@api_view(['GET'])
def course_search(request):
	dept = request.GET.get('department')
	c = request.GET.get('course')
	if dept and c:
		courses = Course.objects.filter(Q(course_id__icontains=c) | Q(course_name__icontains=c), department__id=dept)[:6]
	else:
		courses = None

	serializer = CourseSerializer(courses, many=True)
	return Response(serializer.data)


# add_to_plan_view
# Parameters:-
# course(string): the course id to be added to the plan.
# semester(string, int, int): a tuple of (semetester, year, year + 1) of the choosen semester in the plan.
# Returns:-
# not_passed: If there was a courses that weren't pass yet before the chosen course
# added_to_plan: If the course was added to the plan without any problems.
# It returns these values to the planner_view

@api_view(['POST'])
def add_to_plan_view(request):
	course = request.POST.get('course')
	semester = request.POST.get('semester')
	year = request.POST.get('year')
	
	if not year or not semester or not course:
		return Response({'Error': 'Error in post request'}, status=405)

	context = {}
	try:
		not_passed = check_requisites(request.user.student, course, semester, year)
		context['semester'] = (semester, year, int(year)+1)
	except:
		return Response({'Error': 'Error in not passed'}, status=404)

	if not_passed:
		return Response({'not_passed': True, 'courses': not_passed})

	else:
		try:
			s = StudentCoursePlan(student=request.user.student, course_id=course, semester=get_sem_number(semester), year=year)
			s.save()
		except:
			return Response({'already added': True}) # Return Later

	serializer = CourseSerializer(s.course, many=False)
	return Response(serializer.data)

def remove_from_planner(request, course, semester, year):

	c = get_object_or_404(request.user.student.studentcourseplan_set, course__course_id=course, year=year, semester=get_sem_number(semester))
	c.delete()

	data = semester + ' ' + year + ' ' + str(int(year) + 1)
	url = reverse('portal:planner_view') + '?semester=' + data
	return redirect(url)