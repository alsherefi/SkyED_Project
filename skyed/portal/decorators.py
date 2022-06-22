from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('/portal/home')

		return view_func(request, *args, **kwargs)

	return wrapper_func

def admins_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name
			if group == 'admin':
				return view_func(request, *args, **kwargs)
		
		return redirect('/portal/home')
	
	return wrapper_func

def students_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name
			if group == 'student':
				return view_func(request, *args, **kwargs)
		
		return redirect('/portal/home')
	
	return wrapper_func

def instructors_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name
			if group == 'instructor':
				return view_func(request, *args, **kwargs)

		return redirect('/portal/home')
	
	return wrapper_func
