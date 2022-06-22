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
def schedule_view(request):
	context = {

	}
	return render(request, 'portal/instructor/schedule.html', context)