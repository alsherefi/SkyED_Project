from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from portal.utils import render_to_pdf
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
from datetime import datetime, timedelta, date

def duration(section):
	hours = section.end_time.hour - section.start_time.hour

	if section.end_time.minute > 0:
		return 1 + hours
	return hours

@login_required(login_url='/portal/login')
@students_only
def my_schedule_view(request, sem):
	sections = None
	if sem == 0:
		cs = get_object_or_404(Semester, status=1)
		sections = request.user.student.section_set.filter(semester=cs).order_by('start_time')
		sem = cs.id
		if sections:
			sem = sections[0].semester.id
	else:
		sections = request.user.student.section_set.filter(semester__id=sem).order_by('start_time')


	sun = []
	mon = []
	tue = []
	wed = []
	thu = []

	colors_list = [dict() for i in range(len(sections))]
	colors = ["rose", "violet", "neutral", "amber", "emerald", "cyan", "pink", "teal", "fuchsia"]

	for i, section in enumerate(sections):
		r = i % len(colors)
		colors_list[i] = colors[r]
		if '1' in section.days:
			sun.append({
				'sec':section,
				'color': colors_list[i],
				'row': section.start_time.hour - 6,
				'len':duration(section)
				})

		if '2' in section.days:
			mon.append({
				'sec':section,
				'color': colors_list[i],
				'row': section.start_time.hour - 6,
				'len':duration(section)
				})

		if '3' in section.days:
			tue.append({
				'sec':section,
				'color': colors_list[i],
				'row': section.start_time.hour - 6,
				'len':duration(section)
				})

		if '4' in section.days:
			wed.append({
				'sec':section,
				'color': colors_list[i],
				'row': section.start_time.hour - 6,
				'len':duration(section)
				})

		if '5' in section.days:
			thu.append({
				'sec':section,
				'color': colors_list[i],
				'row': section.start_time.hour - 6,
				'len':duration(section)
				})

	first_semester = request.user.student.semester.registration_starts
	semesters = Semester.objects.filter(Q(registration_starts__gte=first_semester, id__in=(request.user.student.section_set.all().values_list('semester__id', flat=True))) | Q(status=1)).order_by('year', 'semester')
	time_list = ['8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM']
	weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu']
	context = {
		'sun': sun,
		'mon': mon,
		'tue': tue,
		'wed': wed,
		'thu': thu,
		'sections': sections,
		'semesters': semesters,
		'rows': zip(range(2, 15), time_list),
		'columns': range(1, 7),
		'weekdays': zip(range(2, 7), weekdays),
		'sem_id': sem,
	}
	return render(request, 'portal/student/my_schedule.html', context)

	# context['request'] = request
	# pdf = render_to_pdf('portal/student/my_schedule.html', context)

	# response = HttpResponse(pdf, content_type='application/pdf')
	# filename = "My Schedule for " + str(Semester.objects.get(status=1)) + ".pdf"
	# content = "attachment; filename=%s" %(filename)
	# response['Content-Disposition'] = content
	# return response