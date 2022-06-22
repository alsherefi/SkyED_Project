from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(source='login.first_name', read_only=True)
	middle_name = serializers.CharField(source='login.middle_name', read_only=True)
	last_name = serializers.CharField(source='login.last_name', read_only=True)

	class Meta:
		model = Student
		fields = [
			'first_name',
			'middle_name',
			'last_name',
			'registration_id',
		]

class InstructorSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(source='login.first_name', read_only=True)
	last_name = serializers.CharField(source='login.last_name', read_only=True)
	department = serializers.CharField(source='dept.name', read_only=True)

	class Meta:
		model = Instructor
		exclude = ['login', 'dept']

class CourseSerializer(serializers.ModelSerializer):
	department = serializers.CharField(source='department.name', read_only=True)
	class Meta:
		model = Course
		exclude = ['requisites', 'students']

class SemesterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Semester
		fields = [
			'year',
			'semester',
		]

class SectionSerializer(serializers.ModelSerializer):
	course = CourseSerializer(many=False, read_only=True)
	instructor = InstructorSerializer(many=False, read_only=True)
	semester = SemesterSerializer(many=False, read_only=True)

	class Meta:
		model = Section
		exclude = ['students']

class CollegeSerilizer(serializers.ModelSerializer):
	class Meta:
		models = College
		fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
	college = CollegeSerilizer(many=False, read_only=True)
	manager = InstructorSerializer(many=False, read_only=True)

	class Meta:
		model = Department
		fields = '__all__'

class DeptAnnouncementSerializer(serializers.ModelSerializer):
	department = DepartmentSerializer(many=False, read_only=True)
	class Meta:
		model = DeptAnnouncement
		exclude = ['logins']

class SectionAnnouncementSerializer(serializers.ModelSerializer):
	section = SectionSerializer(many=False, read_only=True)
	class Meta:
		model = SectionAnnouncement
		exclude = ['logins']

class GradedStudentSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(source='student.login.first_name', read_only=True)
	middle_name = serializers.CharField(source='student.login.middle_name', read_only=True)
	last_name = serializers.CharField(source='student.login.last_name', read_only=True)
	registration_id = serializers.CharField(source='student.registration_id', read_only=True)
	class Meta:
		model = StudentSection
		fields = ['first_name', 'middle_name', 'last_name', 'registration_id', 'grade']