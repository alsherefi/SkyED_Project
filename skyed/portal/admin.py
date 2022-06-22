from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import *

class StudentAdminModel(admin.ModelAdmin):
	search_fields = ('login__email', 'login__first_name', 'login__last_name', 'registration_id')

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = Login
		fields = ('email', 'first_name', 'middle_name', 'last_name', 'groups', 'is_admin', 'is_superuser')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
				raise ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
				user.save()
		return user

class UserChangeForm(forms.ModelForm):

	password = ReadOnlyPasswordHashField()
	class Meta:
		model = Login
		fields = ('email', 'password', 'first_name', 'middle_name', 'last_name', 'groups', 'is_active', 'is_admin', 'is_superuser')


class LoginAdmin(BaseUserAdmin):
	# The forms to add and change user instances
	form = UserChangeForm
	add_form = UserCreationForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('email', 'first_name', 'last_name', 'is_admin', 'date_joined')
	list_filter = ('is_admin',)
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('first_name', 'middle_name', 'last_name',)}),
		('Permissions', {'fields': ('is_admin', 'is_superuser', 'groups',)}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
				'classes': ('wide',),
				'fields': ('email', 'first_name', 'middle_name', 'last_name', 'groups', 'password1', 'password2'),
		}),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

class DocumentAdmin(admin.ModelAdmin):
  search_fields = ['login__first_name', 'login__last_name', 'login__student__registration_id', 'semester__semester', 'semester__year', 'doc_type']

class InstructorAdmin(admin.ModelAdmin):
	search_fields = ['login__first_name', 'login__last_name', 'registration_id']

class DepartmentAdmin(admin.ModelAdmin):
	search_fields = ['name', 'college__college_name']

class DeptAnnouncementAdmin(admin.ModelAdmin):
	search_fields = ['department__name', 'title', 'adate']
	list_display = ['department', 'title', 'adate', 'status']

class AnnouncementAdmin(admin.ModelAdmin):
	search_fields = ['college__college_name', 'title', 'adate']
	list_display = ['college', 'title', 'adate', 'status']

class CollegeAdmin(admin.ModelAdmin):
	search_fields = ['college_name']
	list_display = ['college_name', 'dean']

class ProgramAdmin(admin.ModelAdmin):
	search_fields = ['title', 'year', 'ptype', 'department__name']
	list_display = ['title', 'year', 'ptype', 'department']

class CourseAdmin(admin.ModelAdmin):
	search_fields = ['course_id', 'course_name', 'department__name']
	list_display = ['course_id', 'course_name', 'department']

class SemesterAdmin(admin.ModelAdmin):
	search_fields = ['semester', 'year', 'status']
	list_display = ['year', 'semester', 'status']

class SectionAdmin(admin.ModelAdmin):
	search_fields = ['course__course_name', 'course__course_id', 'snumber', 'instructor__login__first_name', 'instructor__login__last_name']
	list_display = ['course', 'snumber', 'semester', 'start_time', 'end_time', 'instructor']

class SectionAnnouncementAdmin(admin.ModelAdmin):
	search_fields = ['section__course__course_name', 'section__course__course_id', 'section__snumber', 'section__instructor__login__first_name', 'section__instructor__login__last_name']
	list_display = ['section', 'title', 'adate', 'status']

class StudentCoursePlanAdmin(admin.ModelAdmin):
	search_fields = ['student__login__first_name', 'student__login__last_name', 'student__registration_id', 'course__course_id', 'course__course_name', 'semester', 'year']
	list_display = ['student', 'course', 'year', 'semester']

class StudentSectionAdmin(admin.ModelAdmin):
	search_fields = ['student__login__first_name', 'student__login__last_name', 'student__registration_id', 'section__course__course_id', 'section__course__course_name', 'section__semester__semester', 'section__semester__year']
	list_display = ['student', 'section', 'grade']

class CourseRequisiteAdmin(admin.ModelAdmin):
	search_fields = ['course__course_name', 'course__course_id']

class SegmentAdmin(admin.ModelAdmin):
	search_fields = ['name', 'year']
	list_display = ['name', 'year', 'segment_type']

# Register your models here.
admin.site.register(Login, LoginAdmin)
admin.site.register(Student, StudentAdminModel)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Program,ProgramAdmin)
admin.site.register(DeptAnnouncement, DeptAnnouncementAdmin)
admin.site.register(College, CollegeAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(SectionAnnouncement, SectionAnnouncementAdmin)
admin.site.register(StudentCoursePlan, StudentCoursePlanAdmin)
admin.site.register(StudentSection, StudentSectionAdmin)
admin.site.register(CourseRequisite, CourseRequisiteAdmin)
admin.site.register(Segment, SegmentAdmin)