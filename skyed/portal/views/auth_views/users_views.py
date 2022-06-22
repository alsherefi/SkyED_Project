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

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password= password)
        if user is not None:
            login(request, user)
            return redirect ('/portal/home')
        else:
            return render(request, 'portal/index.html', {'doesnt_exist': True, 'email': email})

    else:
        #form = AuthenticationForm()
        return render(request, 'portal/index.html')

@login_required(login_url='/portal/login')
def home(request):
    group = None
    if request.user.groups.exists():
        print(group)
        group = request.user.groups.all()[0].name
        if group == 'admin':
            return redirect('/admin')
        elif group == 'student':
            return redirect('portal:student_homepage')
        elif group == 'instructor':
            return redirect('portal:instructors_homepage')
    return HttpResponse('<h1>Undefined User</h1>')

def logout_view(request):
    logout(request)
    return redirect('/portal/login')