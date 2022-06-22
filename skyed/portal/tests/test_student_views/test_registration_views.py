from django.test import TestCase, Client

import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import *
from datetime import datetime, timedelta

from django.contrib.auth import login, authenticate, logout
from django.db.models import Q

# Create your tests here.



class TestRegistrationViews(APITestCase):
	def setUp(self):
		self.client = Client()
		self.college = College.objects.create(id="123", college_name="SCI")
		self.department = Department.objects.create(id="456", college = self.college, name="CS")

		self.user = Login.objects.create_user(email="test@student.com", first_name="Jasim", middle_name="Jasom", last_name="Almjsm", password="123kdcow")
		self.user2 = Login.objects.create_user(email="test@instructor.com", first_name="Ahamd", middle_name="A B C", last_name="Alahmadi", password="123kdcow")

		self.group = Group.objects.create(name='student')
		self.instructor_group = Group.objects.create(name='instructor')

		now = datetime.now()

		self.user.groups.add(Group.objects.get(name='student'))
		self.semester = Semester.objects.create(year=2022, semester=2, registration_starts=now - timedelta(days=10), registration_ends=now + timedelta(days=30), grading_deadline=now + timedelta(days=90), exams_starts=now + timedelta(days=80), exams_ends=now + timedelta(days=88), semester_starts = now + timedelta(days=30), semester_ends=now + timedelta(days=90), status=1)

		self.student = Student.objects.create(login = self.user, sex = "M", passed_terms=3, registration_id="2111111", semester = self.semester ,status=1)
		self.instructor = Instructor.objects.create(login = self.user2, registration_id="2111110", dept=self.department)

	def test_registration_GET(self):
		self.client.login(email="test@student.com", password="123kdcow")
		response = self.client.get(reverse('portal:registration_view'))

		self.assertEquals(response.status_code, 200)

	def test_registration_GET_nouser(self):
		response = self.client.get(reverse('portal:registration_view'))

		self.assertRedirects(response, '/portal/login?next=/portal/student/registration/', status_code=302, target_status_code=301, msg_prefix='', fetch_redirect_response=True)
	
	def test_registration_GET_notstudent(self):
		self.client.login(email="test@instructor.com", password="123kdcow")
		response = self.client.get(reverse('portal:registration_view'))

		self.assertRedirects(response, '/portal/home', status_code=302, target_status_code=301, msg_prefix='', fetch_redirect_response=True)

	def test_show_sections_GET_nodata(self):
		self.client.login(email="test@student.com", password="123kdcow")
		response = self.client.get(reverse('portal:show_sections'))

		content = json.loads(response.content)

		self.assertEquals(content, [])
		self.assertEquals(response.status_code, 200)

	def test_show_sections_GET(self):
		self.client.login(email="test@student.com", password="123kdcow")
		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		now = datetime.now()

		section = Section.objects.create(course=course, snumber='01A', semester=self.semester, days='135', start_time='11:00', end_time='11:50')
		section2 = Section.objects.create(course=course, snumber='02A', semester=self.semester, days='24', start_time='11:00', end_time='11:50')

		response = self.client.get(reverse('portal:show_sections'), {'json_course': "0418141"}, format="json")

		self.assertEquals(response.status_code, 200)

		content = json.loads(response.content)

		self.assertEquals(content[0]['course']['course_id'], '0418141')
		self.assertEquals(content[1]['course']['course_id'], '0418141')
		self.assertEquals(response.status_code, 200)

	def test_add_sections_GET(self):
			self.client.login(email="test@student.com", password="123kdcow")
			response = self.client.get(reverse('portal:add_section'), format="json")

			self.assertEquals(response.status_code, 405)

	def test_add_sections_POST_nodata(self):
			self.client.login(email="test@student.com", password="123kdcow")
			response = self.client.post(reverse('portal:add_section'), format='json')

			content = json.loads(response.content)
			self.assertEquals(content, 'no_json_sec_id')
			self.assertEquals(response.status_code, 200)

	def test_add_sections_POST(self):
			self.client.login(email="test@student.com", password="123kdcow")
			course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

			now = datetime.now()

			section = Section.objects.create(course=course, snumber='01A', semester=self.semester, days='135', start_time='11:00', end_time='11:50')

			response = self.client.post(reverse('portal:add_section'), {'json_sec_id': section.id}, format='json')


			content = json.loads(response.content)

			self.assertEquals(response.status_code, 200)
			self.assertEquals(content['condition'], 'Added Successfully')
	
	def test_add_sections_POST_time_conflict(self):
			self.client.login(email="test@student.com", password="123kdcow")

			course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)
			course2 = Course.objects.create(course_id="0418142", course_name="Programming 2", credits=4, department=self.department)

			now = datetime.now()
 
			section = Section.objects.create(course=course, snumber='01A', semester=self.semester, days='135', start_time='11', end_time='11:50')

			section2 = Section.objects.create(course=course2, snumber='02A', semester=self.semester, days='135', start_time='11', end_time='11:50')

			self.student.section_set.add(section)
			s2 = self.user.student.section_set.filter(Q(start_time__range=(section.start_time, section.end_time)) | Q(end_time__range=(section.start_time, section.end_time)), days=section.days, semester=section.semester).values_list('course__course_name', flat=True)

			response = self.client.post(reverse('portal:add_section'), {'json_sec_id': section2.id}, format='json')


			content = json.loads(response.content)

			self.assertEquals(response.status_code, 200)
			self.assertEquals(content['condition'], 'Time conflict')

	def test_add_sections_POST_already_added(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		now = datetime.now()

		section = Section.objects.create(course=course, snumber='01A', semester=self.semester, days='135', start_time='11:00', end_time='11:50')

		section2 = Section.objects.create(course=course, snumber='02A', semester=self.semester, days='24', start_time='11:00', end_time='11:50')

		self.student.section_set.add(section)

		response = self.client.post(reverse('portal:add_section'), {'json_sec_id': section2.id}, format='json')


		content = json.loads(response.content)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(content['condition'], 'Already Added')

	def test_add_sections_POST_already_passed(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		now = datetime.now()

		old_semester = Semester.objects.create(year=2022, semester=1, registration_starts=now - timedelta(days = 30 * 4), registration_ends=now + timedelta(days=30) - timedelta(days = 30 * 4), grading_deadline=now - timedelta(days = 30 * 4) + timedelta(days=90), exams_starts=now - timedelta(days = 30 * 4) + timedelta(days=80), exams_ends=now - timedelta(days = 30 * 4) + timedelta(days=88), semester_starts = now + timedelta(days=30) - timedelta(days = 30 * 4), semester_ends=now + timedelta(days=90) - timedelta(days = 30 * 4), status=2)

		section = Section.objects.create(course=course, snumber='01A', semester=old_semester, days='135', start_time='11:00', end_time='11:50')

		section2 = Section.objects.create(course=course, snumber='02A', semester=self.semester, days='24', start_time='11:00', end_time='11:50')

		studentsection = StudentSection.objects.create(student=self.student, section=section, grade='C')

		response = self.client.post(reverse('portal:add_section'), {'json_sec_id': section2.id}, format='json')


		content = json.loads(response.content)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(content['condition'], 'Already Passed')

	def test_add_sections_POST_already_passed_less_than_C(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		now = datetime.now()

		old_semester = Semester.objects.create(year=2022, semester=1, registration_starts=now - timedelta(days = 30 * 4), registration_ends=now + timedelta(days=30) - timedelta(days = 30 * 4), grading_deadline=now - timedelta(days = 30 * 4) + timedelta(days=90), exams_starts=now - timedelta(days = 30 * 4) + timedelta(days=80), exams_ends=now - timedelta(days = 30 * 4) + timedelta(days=88), semester_starts = now + timedelta(days=30) - timedelta(days = 30 * 4), semester_ends=now + timedelta(days=90) - timedelta(days = 30 * 4), status=2)

		section = Section.objects.create(course=course, snumber='01A', semester=old_semester, days='135', start_time='11:00', end_time='11:50')

		section2 = Section.objects.create(course=course, snumber='02A', semester=self.semester, days='24', start_time='11:00', end_time='11:50')

		studentsection = StudentSection.objects.create(student=self.student, section=section, grade='D+')

		response = self.client.post(reverse('portal:add_section'), {'json_sec_id': section2.id}, format='json')


		content = json.loads(response.content)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(content['condition'], 'Added Successfully')

	def test_add_sections_POST_failed_to_pass(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		now = datetime.now()

		old_semester = Semester.objects.create(year=2022, semester=1, registration_starts=now - timedelta(days = 30 * 4), registration_ends=now + timedelta(days=30) - timedelta(days = 30 * 4), grading_deadline=now - timedelta(days = 30 * 4) + timedelta(days=90), exams_starts=now - timedelta(days = 30 * 4) + timedelta(days=80), exams_ends=now - timedelta(days = 30 * 4) + timedelta(days=88), semester_starts = now + timedelta(days=30) - timedelta(days = 30 * 4), semester_ends=now + timedelta(days=90) - timedelta(days = 30 * 4), status=2)

		section = Section.objects.create(course=course, snumber='01A', semester=old_semester, days='135', start_time='11:00', end_time='11:50')

		section2 = Section.objects.create(course=course, snumber='02A', semester=self.semester, days='24', start_time='11:00', end_time='11:50')

		studentsection = StudentSection.objects.create(student=self.student, section=section, grade='F')

		response = self.client.post(reverse('portal:add_section'), {'json_sec_id': section2.id}, format='json')

		content = json.loads(response.content)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(content['condition'], 'Added Successfully')

	def test_add_sections_POST_more_than_twice(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		now = datetime.now()

		old_semester = Semester.objects.create(year=2022, semester=1, registration_starts=now - timedelta(days = 30 * 4), registration_ends=now + timedelta(days=30) - timedelta(days = 30 * 4), grading_deadline=now - timedelta(days = 30 * 4) + timedelta(days=90), exams_starts=now - timedelta(days = 30 * 4) + timedelta(days=80), exams_ends=now - timedelta(days = 30 * 4) + timedelta(days=88), semester_starts = now + timedelta(days=30) - timedelta(days = 30 * 4), semester_ends=now + timedelta(days=90) - timedelta(days = 30 * 4), status=2)

		older_semester = Semester.objects.create(year=2021, semester=2, registration_starts=now - timedelta(days = 30 * 8), registration_ends=now + timedelta(days=30) - timedelta(days = 30 * 4), grading_deadline=now - timedelta(days = 30 * 8) + timedelta(days=90), exams_starts=now - timedelta(days = 30 * 8) + timedelta(days=80), exams_ends=now - timedelta(days = 30 * 8) + timedelta(days=88), semester_starts = now + timedelta(days=30) - timedelta(days = 30 * 8), semester_ends=now + timedelta(days=90) - timedelta(days = 30 * 8), status=2)

		section = Section.objects.create(course=course, snumber='01A', semester=older_semester, days='135', start_time='11:00', end_time='11:50')

		section2 = Section.objects.create(course=course, snumber='01A', semester=old_semester, days='135', start_time='11:00', end_time='11:50')

		section3 = Section.objects.create(course=course, snumber='02A', semester=self.semester, days='24', start_time='11:00', end_time='11:50')


		studentsection = StudentSection.objects.create(student=self.student, section=section, grade='C-')

		studentsection = StudentSection.objects.create(student=self.student, section=section2, grade='F')

		response = self.client.post(reverse('portal:add_section'), {'json_sec_id': section3.id}, format='json')

		content = json.loads(response.content)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(content['condition'], 'Added Successfully')


	def test_add_sections_POST_faild_once_passed_the_second_time(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		now = datetime.now()

		old_semester = Semester.objects.create(year=2022, semester=1, registration_starts=now - timedelta(days = 30 * 4), registration_ends=now + timedelta(days=30) - timedelta(days = 30 * 4), grading_deadline=now - timedelta(days = 30 * 4) + timedelta(days=90), exams_starts=now - timedelta(days = 30 * 4) + timedelta(days=80), exams_ends=now - timedelta(days = 30 * 4) + timedelta(days=88), semester_starts = now + timedelta(days=30) - timedelta(days = 30 * 4), semester_ends=now + timedelta(days=90) - timedelta(days = 30 * 4), status=2)

		older_semester = Semester.objects.create(year=2021, semester=2, registration_starts=now - timedelta(days = 30 * 8), registration_ends=now + timedelta(days=30) - timedelta(days = 30 * 4), grading_deadline=now - timedelta(days = 30 * 8) + timedelta(days=90), exams_starts=now - timedelta(days = 30 * 8) + timedelta(days=80), exams_ends=now - timedelta(days = 30 * 8) + timedelta(days=88), semester_starts = now + timedelta(days=30) - timedelta(days = 30 * 8), semester_ends=now + timedelta(days=90) - timedelta(days = 30 * 8), status=2)

		section = Section.objects.create(course=course, snumber='01A', semester=older_semester, days='135', start_time='11:00', end_time='11:50')

		section2 = Section.objects.create(course=course, snumber='01A', semester=old_semester, days='135', start_time='11:00', end_time='11:50')

		section3 = Section.objects.create(course=course, snumber='02A', semester=self.semester, days='24', start_time='11:00', end_time='11:50')


		studentsection = StudentSection.objects.create(student=self.student, section=section, grade='C-')

		studentsection = StudentSection.objects.create(student=self.student, section=section2, grade='A')

		response = self.client.post(reverse('portal:add_section'), {'json_sec_id': section3.id}, format='json')

		content = json.loads(response.content)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(content['condition'], 'Already Passed')

	def test_add_sections_POST_prequisite_required(self):
			self.client.login(email="test@student.com", password="123kdcow")
			course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)
			course2 = Course.objects.create(course_id="0418142", course_name="Programming 2", credits=4, department=self.department)

			CourseRequisite.objects.create(course=course2, requisite=course, requisite_type='prerequisite')

			now = datetime.now()

			section = Section.objects.create(course=course2, snumber='01A', semester=self.semester, days='135', start_time='11:00', end_time='11:50')

			response = self.client.post(reverse('portal:add_section'), {'json_sec_id': section.id}, format='json')


			content = json.loads(response.content)

			self.assertEquals(response.status_code, 200)
			self.assertEquals(content['condition'], 'Prerequisites not passed')


	def test_remove_section_GET(self):
		self.client.login(email="test@student.com", password="123kdcow")
		response = self.client.get(reverse('portal:remove_section'), format="json")

		self.assertEquals(response.status_code, 405)

	def test_remove_section_no_data_POST(self):
		self.client.login(email="test@student.com", password="123kdcow")
		response = self.client.post(reverse('portal:remove_section'), format="json")

		self.assertEquals(response.status_code, 400)

		content = json.loads(response.content)

		self.assertEquals(response.status_code, 400)
		self.assertEquals(content['cond'], 0)


	def test_remove_section_POST_doesnt_exist(self):
		self.client.login(email="test@student.com", password="123kdcow")
		response = self.client.post(reverse('portal:remove_section'), {'sid': -1}, format="json")

		content = json.loads(response.content)

		self.assertEquals(response.status_code, 400)
		self.assertEquals(content['cond'], 1)

	def test_remove_section_POST_success(self):
		self.client.login(email="test@student.com", password="123kdcow")

		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		now = datetime.now()

		section = Section.objects.create(course=course, snumber='01A', semester=self.semester, days='135', start_time='11:00', end_time='11:50')

		s = StudentSection.objects.create(student=self.student, section=section)


		response = self.client.post(reverse('portal:remove_section'), {'sid': s.section_id}, format="json")

		self.assertEquals(response.status_code, 200)
