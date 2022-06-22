from django.test import TestCase, Client

import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import *
from datetime import datetime, timedelta

from django.contrib.auth import login, authenticate, logout
import json

# Create your tests here.



class TestMakeAnnouncement(APITestCase):
	def setUp(self):
		self.client = Client()
		self.college = College.objects.create(id="123", college_name="SCI")
		self.department = Department.objects.create(id="456", college = self.college, name="CS")

		self.user2 = Login.objects.create_user(email="test@student.com", first_name="Jasim", middle_name="Jasom", last_name="Almjsm", password="123kdcow")
		self.user = Login.objects.create_user(email="test@instructor.com", first_name="Ahamd", middle_name="A B C", last_name="Alahmadi", password="123kdcow")

		self.group = Group.objects.create(name='student')
		self.instructor_group = Group.objects.create(name='instructor')

		now = datetime.now()

		self.user2.groups.add(Group.objects.get(name='student'))
		self.user.groups.add(Group.objects.get(name='instructor'))
		self.semester = Semester.objects.create(year=2022, semester=2, registration_starts=now - timedelta(days=10), registration_ends=now + timedelta(days=30), grading_deadline=now + timedelta(days=90), exams_starts=now + timedelta(days=80), exams_ends=now + timedelta(days=88), semester_starts = now + timedelta(days=30), semester_ends=now + timedelta(days=90), status=1)

		self.student = Student.objects.create(login = self.user2, sex = "M", passed_terms=3, registration_id="2111111", semester = self.semester ,status=1)
		self.instructor = Instructor.objects.create(login = self.user, registration_id="2111110", dept=self.department)


	
	def test_make_announcement_GET_nouser(self):
		response = self.client.get(reverse('portal:make_announcement'))

		self.assertRedirects(response, '/portal/login?next=/portal/instructor/make_announcement/', status_code=302, target_status_code=301, msg_prefix='', fetch_redirect_response=True)

	def test_make_announcements_GET_notinstructor(self):
		self.client.login(email="test@student.com", password="123kdcow")
		response = self.client.get(reverse('portal:make_announcement'))

		self.assertRedirects(response, '/portal/home', status_code=302, target_status_code=301, msg_prefix='', fetch_redirect_response=True)
	
	def test_make_announcements_GET(self):
		self.client.login(email="test@instructor.com", password="123kdcow")
		response = self.client.get(reverse('portal:make_announcement'))

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'portal/instructor/make_announcement.html')

	def test_make_announcements_GET_no_semester(self):
		self.client.login(email="test@instructor.com", password="123kdcow")
		self.semester.delete()
		response = self.client.get(reverse('portal:make_announcement'))

		self.assertEquals(response.status_code, 200)