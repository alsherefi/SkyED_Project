from .models import *
from django import forms

class CourseForm(forms.ModelForm):
	course = forms.CharField(max_length=200)

	class Meta:
		model = Course
		fields = [
			'department',
			'course',
		]