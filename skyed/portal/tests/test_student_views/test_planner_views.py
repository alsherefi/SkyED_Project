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



class TestPlannerViews(APITestCase):
	def setUp(self):
		self.client = Client()
		self.college = College.objects.create(id="123", college_name="SCI")
		self.department = Department.objects.create(id="456", college = self.college, name="CS")

		self.user = Login.objects.create_user(email="test@student.com", first_name="Jasim", middle_name="Jasom", last_name="Almjsm", password="123kdcow")
		self.user2 = Login.objects.create_user(email="test@instructor.com", first_name="Ahamd", middle_name="A B C", last_name="Alahmadi", password="123kdcow")

		self.group = Group.objects.create(name='student')
		self.instructor_group = Group.objects.create(name='instructor')

		self.user.groups.add(Group.objects.get(name='student'))
		self.semester = Semester.objects.create(year=2022, semester=2, registration_starts=datetime.now() - timedelta(days=10), registration_ends=datetime.now() + timedelta(days=30), grading_deadline=datetime.now() + timedelta(days=90), exams_starts=datetime.now() + timedelta(days=80), exams_ends=datetime.now() + timedelta(days=88), semester_starts = datetime.now() + timedelta(days=30), semester_ends=datetime.now() + timedelta(days=90), status=1)

		self.student = Student.objects.create(login = self.user, sex = "M", passed_terms=3, registration_id="2111111", semester = self.semester ,status=1)
		self.instructor = Instructor.objects.create(login = self.user2, registration_id="2111110", dept=self.department)


	def test_planner_GET(self):
		self.client.login(email="test@student.com", password="123kdcow")
		response = self.client.get(reverse('portal:planner_view'))

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'portal/student/zplanner.html')

	def test_planner_GET_nouser(self):
		response = self.client.get(reverse('portal:planner_view'))

		self.assertRedirects(response, '/portal/login?next=/portal/student/planner/', status_code=302, target_status_code=301, msg_prefix='', fetch_redirect_response=True)


	def test_planner_GET_notstudent(self):
		self.client.login(email="test@instructor.com", password="123kdcow")
		response = self.client.get(reverse('portal:planner_view'))

		self.assertRedirects(response, '/portal/home', status_code=302, target_status_code=301, msg_prefix='', fetch_redirect_response=True)


	def test_planner_GET_empty_semester(self):
		self.client.login(email="test@student.com", password="123kdcow")
		response = self.client.get(reverse('portal:planner_view'), {
			'semester': 'Spring 2024 2025', 
		})

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'portal/student/zplanner.html')

	def test_planner_GET_semester(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		StudentCoursePlan.objects.create(student=self.student, course=course, semester=2, year=2024)

		response = self.client.get(reverse('portal:planner_view'), {
			'semester': 'Spring 2024 2025', 
		})

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'portal/student/zplanner.html')
		self.assertEquals(response.context['student_courses'][0], course)

	def test_planner_GET_semester_no_courses(self):
		self.client.login(email="test@student.com", password="123kdcow")

		response = self.client.get(reverse('portal:planner_view'), {
			'semester': 'Spring 2024 2025', 
		})

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'portal/student/zplanner.html')

	def test_planner_GET_semester_bad_request(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		StudentCoursePlan.objects.create(student=self.student, course=course, semester=2, year=2024)

		response = self.client.get(reverse('portal:planner_view'), {
			'semester': 'wfcabc', 
		})

		self.assertEquals(response.status_code, 302)

	def test_planner_GET_current_semester(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		StudentCoursePlan.objects.create(student=self.student, course=course, semester=2, year=2022)

		response = self.client.get(reverse('portal:planner_view'))

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'portal/student/zplanner.html')
		self.assertEquals(response.context['student_courses'][0], course)

	def test_course_search_GET_no_data(self):
		self.client.login(email="test@student.com", password="123kdcow")

		response = self.client.get(reverse('portal:course_search'), format='json')

		content = json.loads(response.content)

		self.assertEquals(response.status_code, 200)
		print(content)
		# self.assertEquals(content['course'])

	def test_course_search_GET_wrong_data(self):
		self.client.login(email="test@student.com", password="123kdcow")

		response = self.client.get(reverse('portal:course_search'), {
			'dept': 'abc',
			'c': '123'
		}, format='json')

		content = json.loads(response.content)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(content, [])

	def test_course_search_GET(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		response = self.client.get(reverse('portal:course_search'), {
			'department': self.department.id,
			'course': 'prog'
		}, format='json')

		content = json.loads(response.content)

		print(content)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(content[0]['course_id'], course.course_id)

	def test_add_to_plan_POST_bad_request(self):
		self.client.login(email="test@student.com", password="123kdcow")

		response = self.client.post(reverse('portal:add_to_plan_view'), format='json')

		self.assertEquals(response.status_code, 405)
	
	def test_add_to_plan_POST_bad_request2(self):
		response = self.client.post(reverse('portal:add_to_plan_view'), {
			'year': 'abc',
			'course': 'efg',
			'semester': 'xyz',
		}, format='json')

		self.assertEquals(response.status_code, 405)

	def test_add_to_plan_POST_already_added(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		StudentCoursePlan.objects.create(student=self.student, course=course, year=2023, semester=1)

		response = self.client.post(reverse('portal:add_to_plan_view'), {
			'year': 2023,
			'course': course.course_id,
			'semester': 'Fall',
		}, format='json')

		content = json.loads(response.content)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(content['already added'], True)

	def test_add_to_plan_POST_not_passed(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		course0 = Course.objects.create(course_id="041814test", course_name="Programming test", credits=4, department=self.department)
	
		course2 = Course.objects.create(course_id="0418142", course_name="Programming 2", credits=4, department=self.department)

		CourseRequisite.objects.create(course=course2, requisite=course, requisite_type='prerequisite')
		CourseRequisite.objects.create(course=course2, requisite=course0, requisite_type='prerequisite')

		response = self.client.post(reverse('portal:add_to_plan_view'), {
			'year': 2023,
			'course': course2.course_id,
			'semester': 'Fall',
		}, format='json')

		content = json.loads(response.content)
		print(content)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(content['not_passed'], True)
		self.assertEquals(content['courses'], [['0418141', 'Programming 1'], ['041814test', 'Programming test']])
	
	def test_add_to_plan_POST(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)	

		response = self.client.post(reverse('portal:add_to_plan_view'), {
			'year': 2023,
			'course': course.course_id,
			'semester': 'Fall',
		}, format='json')

		content = json.loads(response.content)
		print(content)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(content['course_id'], course.course_id)
