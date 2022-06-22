from django.test import TestCase, Client

import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import *
from datetime import datetime, timedelta

from django.contrib.auth import login, authenticate, logout

class TestHomepageVew(APITestCase):
	def setUp(self):
		self.client = Client()
		self.college = College.objects.create(id="123", college_name="SCI")
		self.department = Department.objects.create(id="456", college = self.college, name="CS")
		# self.course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		self.user = Login.objects.create_user(email="test@student.com", first_name="Jasim", middle_name="Jasom", last_name="Almjsm", password="123kdcow")
		self.user2 = Login.objects.create_user(email="test@instructor.com", first_name="Ahamd", middle_name="A B C", last_name="Alahmadi", password="123kdcow")

		self.group = Group.objects.create(name='student')
		self.instructor_group = Group.objects.create(name='instructor')

		self.user.groups.add(Group.objects.get(name='student'))
		self.semester = Semester.objects.create(year=2022, semester=2, registration_starts=datetime.now() - timedelta(days=10), registration_ends=datetime.now() + timedelta(days=30), grading_deadline=datetime.now() + timedelta(days=90), exams_starts=datetime.now() + timedelta(days=80), exams_ends=datetime.now() + timedelta(days=88), semester_starts = datetime.now() + timedelta(days=30), semester_ends=datetime.now() + timedelta(days=90), status=1)

		self.student = Student.objects.create(login = self.user, sex = "M", passed_terms=3, registration_id="2111111", semester = self.semester ,status=1)
		self.instructor = Instructor.objects.create(login = self.user2, registration_id="2111110", dept=self.department)

	def test_student_homepage_GET(self):
		self.client.login(email="test@student.com", password="123kdcow")

		response = self.client.get(reverse('portal:student_homepage'))

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'portal/student/student_homepage.html')

	def test_student_homepage_GET_nouser(self):
		response = self.client.get(reverse('portal:student_homepage'))

		self.assertRedirects(response, '/portal/login?next=/portal/student/student_homepage/', status_code=302, target_status_code=301, msg_prefix='', fetch_redirect_response=True)

	def test_student_homepage_GET_notstudent(self):
		self.client.login(email="test@instructor.com", password="123kdcow")
		response = self.client.get(reverse('portal:student_homepage'))

		self.assertRedirects(response, '/portal/home', status_code=302, target_status_code=301, msg_prefix='', fetch_redirect_response=True)
