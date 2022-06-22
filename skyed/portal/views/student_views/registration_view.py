from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ...decorators import *
from ...models import *
from django.db.models import Q
import datetime
import random
from ...filters import SectionFilter, CourseFilter
from .student_homepage import get_registration_semester
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...serializers import *
from datetime import datetime
from rest_framework import status

@login_required(login_url='/portal/login')
@students_only
def registration_view(request):
	current_time = datetime.now()
	semester = get_registration_semester()
	summery = None
	student = request.user.student
	
	if semester == None or not (semester.registration_starts <= current_time <= semester.registration_ends):
			return render(request, 'portal/student/registration.html', {'not_register_time': True})

	try:
			planner_courses = student.course_set.filter(studentcourseplan__semester=semester.semester, studentcourseplan__year=semester.year)
	except StudentCoursePlan.DoesNotExist:
			planner_courses = None
	
	summery = student.section_set.filter(semester=semester)

	context = {
		"plan": planner_courses,
		'summery': summery
	}
	return render(request, 'portal/student/registration.html', context)
	
	# courses = None
	# if 'course' in request.GET:
	# 	sections = Section.objects.filter(course__course_id=request.GET['course'], semester=semester.semester, year=semester.year)

	# condition = None

	# if request.method == 'POST':
	# 	### There is a better way to do it. (JQuery)
	# 	course_number = request.POST['course_number']
	# 	courses = Course.objects.filter(course_id__icontains=course_number, section__semester=semester.semester, section__year=semester.year).distinct()
	# 	sections = Section.objects.filter(course__course_id=request.POST['course'], semester=semester.semester, year=semester.year)
	# 	#######################################
	# 	section = Section.objects.get(id=int(request.POST['section']))
	# 	requisites = section.course.requisites.filter(requisite__requisite_type='prerequisite')
	# 	old_sections = student.section_set.exclude(semester=semester.semester, year=semester.year)
	# 	old_sections = old_sections.exclude(studentsection__grade__in=('F', 'FA', 'W', 'CW'))

	# 	req = []
	# 	for requisite in requisites:
	# 		if requisite not in old_sections:
	# 			req.append(requisite.__str__())

	# 	s2 = student.section_set.filter(Q(start_time__gte=section.start_time) | Q(end_time__lte=section.start_time), days=section.days, semester=section.semester, year=section.year).values_list('course__course_name', flat=True)

	# 	if req:
	# 		condition = req
	# 	elif s2:
	# 		time_conflict = s2
	# 	else:
	# 		try:
	# 			s = StudentSection.objects.exclude(grade__in=('D', 'D+', 'C-')).get(section__course=section.course, student=student)
	# 			if semester.semester == s.section.semester and semester.year == s.section.year:
	# 				condition = 'Already Added'
	# 			else:
	# 				condition = 'Already Passed'

	# 		except StudentSection.DoesNotExist:
	# 			new_section = StudentSection(section=section, student=student)
	# 			new_section.save()
	# 			condition = 'Added Successfully'


	
	# context = {
	# 	'courses': courses,
	# 	'sections': sections,
	# 	'condition': condition,
	# 	'summery': summery,
	# 	'planner_courses': planner_courses,
	# 	'removed': removed,
	# 	'time_conflict': time_conflict,
	# }

	# return render(request, 'portal/test2.html', context)

@api_view(['GET'])
def show_sections(request):
	semester = get_registration_semester()
	sections = None
	course = request.GET.get("json_course")
	if course:
		sections = Section.objects.filter(course__course_id=course, semester=semester)

	serializer = SectionSerializer(sections, many=True)
	return Response(serializer.data)


@api_view(['POST'])
def ajax_add_section(request):
	semester = get_registration_semester()
	time_conflict = None
	req = None
	section = None

	if request.method == 'POST':
		if request.POST.get('json_sec_id') == None:
			return Response('no_json_sec_id')

		section = Section.objects.get(id=int(request.POST['json_sec_id']))
		requisites = section.course.requisites.filter(requisite__requisite_type='prerequisite')
		old_sections = request.user.student.section_set.exclude(semester=semester)
		old_sections = old_sections.exclude(studentsection__grade__in=('F', 'FA', 'W', 'CW')).values_list('course__course_id', flat=True)

		print(old_sections)
		print(requisites)

		req = []
		for requisite in requisites:
			if requisite.course_id not in old_sections:
				req.append(requisite.__str__())

		s2 = request.user.student.section_set.filter(Q(start_time__range=(section.start_time, section.end_time)) | Q(end_time__range=(section.start_time, section.end_time)), days=section.days, semester=section.semester).values_list('course__course_name', flat=True)

		if req:
			condition = "Prerequisites not passed"
		elif s2:
			time_conflict = s2
			condition = "Time conflict"
			if section.course.course_name in s2:
				condition = "Already Added"
		else:
			try:
				s = StudentSection.objects.exclude(grade__in=('D', 'D+', 'C-', 'F', 'FA')).get(section__course=section.course, student=request.user.student)
				if (semester == s.section.semester) or s.grade == None:
					condition = 'Already Added'
				else:
					condition = 'Already Passed'

			except StudentSection.DoesNotExist:
				new_section = StudentSection(section=section, student=request.user.student)
				new_section.save()
				condition = 'Added Successfully'
	
	# serialized_section = SectionSerializer(section, many=False)

	instructor = section.instructor
	print(instructor)
	if instructor != None:
		instructor = str(instructor.login)

	context = {
		'prerequisites': req,
		'condition': condition,
		'time_conflict': time_conflict,
		'section': {
			'id': section.id,
			'snumber': section.snumber,
			'course': section.course.course_name,
			'instructor': instructor,
			'building': section.building,
			'room': section.room,
			'start_time': section.start_time,
			'end_time': section.end_time,
			'days': section.days,
		},
	}
	return Response(context)


@api_view(['POST'])
def remove_section_view(request):
	sid = request.POST.get('sid')
	print(sid)
	if sid:
		try:
			qs = request.user.student.studentsection_set.get(section__id=sid)
			qs.delete()
		except:
			return Response({'cond': 1}, status=status.HTTP_400_BAD_REQUEST)

		return Response(status=status.HTTP_200_OK)

	return Response({'cond': 0}, status=status.HTTP_400_BAD_REQUEST)