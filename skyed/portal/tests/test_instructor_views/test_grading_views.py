from django.test import TestCase, Client

import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import *
from datetime import datetime, timedelta

from django.contrib.auth import login, authenticate, logout

class TestGradingSection(APITestCase):
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

	def test_show_graded_sections_GET(self):
		self.client.login(email="test@instructor.com", password="123kdcow")
		response = self.client.get(reverse('portal:grading'))

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'portal/instructor/grading.html')

	def test_show_graded_sections_GET_nouser(self):
		response = self.client.get(reverse('portal:grading'))

		self.assertRedirects(response, '/portal/login?next=/portal/instructor/grading/', status_code=302, target_status_code=301, msg_prefix='', fetch_redirect_response=True)
	
	def test_show__graded_sections_GET_notinstructor(self):
		self.client.login(email="test@student.com", password="123kdcow")
		response = self.client.get(reverse('portal:grading'))
	
		self.assertRedirects(response, '/portal/home', status_code=302, target_status_code=301, msg_prefix='', fetch_redirect_response=True)
	
	def test_list_grades_GET_invalid_data(self):
		self.client.login(email="test@instructor.com", password="123kdcow")
		response = self.client.get(reverse('portal:ajax_grades_list'), {'json_sec': 1}, format='json')

		self.assertEquals(response.status_code, 404)

	def test_list_students_GET(self):
		self.client.login(email="test@instructor.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		section = Section.objects.create(course=course, snumber='01A', semester=self.semester, days='135', start_time='11:00', end_time='11:50')

		response = self.client.get(reverse('portal:ajax_grades_list'), {'json_sec': section.id}, format='json')

		self.assertEquals(response.status_code, 200)

	def test_csv_grades_invalid_section(self):
		self.client.login(email="test@instructor.com", password="123kdcow")
		response = self.client.get(reverse('portal:csv_grades_list', args=[1]))

		self.assertEquals(response.status_code, 404)

	def test_csv_grades_GET(self):
		self.client.login(email="test@instructor.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		section = Section.objects.create(course=course, snumber='01A', semester=self.semester, days='135', start_time='11:00', end_time='11:50')

		response = self.client.get(reverse('portal:csv_grades_list', args=[section.id]))

		self.assertEquals(response.status_code, 200)

	def test_csv_grades_GET_nouser(self):
		response = self.client.get(reverse('portal:csv_grades_list', args=[1]))

		self.assertEquals(response.status_code, 302)
	
	def test_csv_grades_GET_notinstructor(self):
		self.client.login(email="test@student.com", password="123kdcow")
		response = self.client.get(reverse('portal:csv_grades_list', args=[1]))
	
		self.assertEquals(response.status_code, 302)

	def test_grading_POST_bad_request(self):
		self.client.login(email="test@instructor.com", password="123kdcow")
		response = self.client.post(reverse('portal:ajax_grading'))
	
		content = json.loads(response.content)

		self.assertEquals(response.status_code, 405)
		self.assertEquals(content['error'], 'grades and sid bad request')

	def test_grading_POST_no_section(self):
		self.client.login(email="test@instructor.com", password="123kdcow")
		response = self.client.post(reverse('portal:ajax_grading'), {
			'json_sec': 1,
			'students_grades': '{"2131110461":"A"}'
		}, format='json')
	
		self.assertEquals(response.status_code, 404)

	def test_grading_POST_empty_section(self):
		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		section = Section.objects.create(course=course, snumber='01A', semester=self.semester, days='135', start_time='11:00', end_time='11:50')

		self.client.login(email="test@instructor.com", password="123kdcow")
		response = self.client.post(reverse('portal:ajax_grading'), {
			'json_sec': section.id,
			'students_grades': '{"2131110461":"A"}'
		}, format='json')
	
		self.assertEquals(response.status_code, 404)

	def test_grading_POST(self):
		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		section = Section.objects.create(course=course, snumber='01A', semester=self.semester, days='135', start_time='11:00', end_time='11:50')

		self.client.login(email="test@instructor.com", password="123kdcow")

		section.students.add(self.user2.student)

		response = self.client.post(reverse('portal:ajax_grading'), {
			'json_sec': section.id,
			'students_grades': f'{{"{self.user2.student.registration_id}":"A"}}'
		}, format='json')
	
		self.assertEquals(response.status_code, 200)
		self.assertEquals(section.studentsection_set.get(student=self.user2.student, grade='A').student, self.user2.student)
	