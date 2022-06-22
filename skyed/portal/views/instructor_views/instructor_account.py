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
def instructor_account_view(request):
	condition = request.session.get('change_password')
	if condition:
			del(request.session['change_password'])
	context = {
			'condition': condition
	}
	return render(request, 'portal/instructor/account.html', context)

@login_required(login_url='/portal/login')
@instructors_only
def inst_change_password(request):
	if request.method == 'POST':
		print('here')
		password = request.POST.get('old_password')
		if authenticate(request, email=request.user.email, password=password):
			new_password = request.POST['new_password']
			request.user.set_password(new_password)
			request.user.save()
			login(request, request.user)
			request.session['change_password'] = True
		else:
			request.session['change_password'] = False

	return redirect('/portal/instructor/account')
