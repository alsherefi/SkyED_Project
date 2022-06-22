from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ...decorators import *
from ...models import *
from django.db.models import F
from ...filters import SectionFilter, CourseFilter
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...serializers import *
from django.http import Http404
from datetime import datetime, timedelta

@login_required(login_url='/portal/login')
@instructors_only
def make_announcement_view(request):
	try:
			manager = request.user.groups.get(name='manager')
	except:
			manager = None

	ismanager = False
	if manager:
			ismanager = True


	announcement_to = []
	current_time = datetime.now()

	sections = request.user.instructor.section_set.filter(semester__status=1)
	dept = request.user.instructor.dept
	college = request.user.instructor.dept.college

	myanns = SectionAnnouncement.objects.filter(section__in=sections).annotate(name=F('section__course__course_name')).values('name', 'title', 'info', 'adate')
	dept_ann = DeptAnnouncement.objects.filter(department=dept, status__in=(1, 3)).annotate(name=F('department__name')).values('name', 'title', 'info', 'adate')
	college_ann = Announcement.objects.filter(college=college, status__in=(1, 3)).annotate(name=F('college__college_name')).values('name','title', 'info', 'adate')

	announcements = dept_ann.union(college_ann).union(myanns).order_by('-adate')

	context = {
		'sections': sections,
		'ismanager': ismanager,
		'announcements': announcements,
	}

	return render(request, 'portal/instructor/make_announcement.html', context)


#TODO
@api_view(['POST'])
def send_announcement_view(request):
	print('here')
	sid = request.POST.get('sid')

	if sid == "D":
		department = request.user.instructor.department
		title = 'Dr. ' + request.user.first_name + ' ' + request.user.last_name
		info = request.POST.get('ann')
		status = request.POST.get('status')

		announcements = DeptAnnouncement.objects.create(department=department, title=title, info=info, status=status)

		serializer = DeptAnnouncementSerializer(announcements, many=False) 
		return Response(serializer.data)

	else:
		sid = request.POST.get('sid')
		title = 'Dr. ' + request.user.first_name + ' ' + request.user.last_name
		info = request.POST.get('ann')

		announcements = SectionAnnouncement.objects.create(section_id=sid, title=title, info=info)
	
		serializer = SectionAnnouncementSerializer(announcements, many=False)
		return Response(serializer.data)
