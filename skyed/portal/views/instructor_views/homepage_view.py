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

# Do queries for the announcements from the department and college. check if these announcements are acknowledged or not.
@login_required(login_url='/portal/login')
@instructors_only
def instructors_homepage_view(request):
	dept = request.user.instructor.dept
	college = request.user.instructor.dept.college

	ack_dept = request.user.deptannouncement_set.all().values_list('id', flat=True)
	ack_college = request.user.announcement_set.all().values_list('id', flat=True)

	sections = request.user.instructor.section_set.filter(semester__status=1)

	myanns = SectionAnnouncement.objects.filter(section__in=sections).annotate(name=F('section__course__course_name')).values('name', 'title', 'info', 'adate')
	dept_ann = DeptAnnouncement.objects.filter(department=dept, status__in=(1, 3)).exclude(id__in=ack_dept).annotate(name=F('department__name')).values('name', 'title', 'info', 'adate')
	college_ann = Announcement.objects.filter(college=college, status__in=(1, 3)).exclude(id__in=ack_college).annotate(name=F('college__college_name')).values('name','title', 'info', 'adate')

	announcements = dept_ann.union(college_ann).union(myanns).order_by('-adate')

	context = {
		'announcements': announcements,
	}

	return render(request, 'portal/instructor/homepage.html', context)
