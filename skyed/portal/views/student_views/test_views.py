from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ...decorators import *
from ...models import *
from django.db.models import F
import datetime
from datetime import datetime, timedelta
from ...filters import SectionFilter, CourseFilter

def test_view(request):
	sections = request.user.student.section_set.filter(semester__status=1).order_by('start_time')
	
	sun = []
	mon = []
	tue = []
	wed = []
	thu = []

	for section in sections:

		if '1' in section.days:
			sun.append(section)

		if '2' in section.days:
			mon.append(section)

		if '3' in section.days:
			tue.append(section)

		if '4' in section.days:
			wed.append(section)

		if '5' in section.days:
			thu.append(section)

	first_semester = request.user.student.semester.registration_starts
	semesters = Semester.objects.filter(registration_starts__gte=first_semester)

	time_list = ['8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM']
	weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu']
	context = {
		'sun': sun,
		'mon': mon,
		'tue': tue,
		'wed': wed,
		'thu': thu,
		'semesters': semesters,
		'rows': zip(range(2, 15), time_list),
		'columns': range(1, 7),
		'weekdays': zip(range(2, 7), weekdays),
	}
	return render(request, 'portal/student/test.html', context)

def soon_view(request):
	context = {}
	return render(request, 'portal/student/soon.html', context)