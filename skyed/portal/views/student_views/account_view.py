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

@login_required(login_url='/portal/login')
@students_only
def account_view(request):
    condition = request.session.get('change_password')
    if condition:
        del(request.session['change_password'])
    context = {
        'condition': condition
    }
    return render(request, 'portal/student/account.html', context)

@login_required(login_url='/portal/login')
@students_only
def change_password_view(request):
    if request.method == 'POST':
        if authenticate(request, email=request.user.email, password=request.POST['old_password']):
            new_password = request.POST['new_password']
            request.user.set_password(new_password)
            request.user.save()
            login(request, request.user)
            request.session['change_password'] = True
        else:
            request.session['change_password'] = False

    return redirect('/portal/student/account')
