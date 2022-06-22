from selenium import webdriver
from portal.models import *
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
from datetime import datetime, timedelta

class TestSkyedInstructor(StaticLiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Chrome('integration_test/chromedriver.exe')
	
		self.college = College.objects.create(id="123", college_name="SCI")
		self.department = Department.objects.create(id="456", college = self.college, name="CS")

		self.user = Login.objects.create_user(email="test@student.com", first_name="Jasim", middle_name="Jasom", last_name="Almjsm", password="itsame")
		self.user2 = Login.objects.create_user(email="test@instructor.com", first_name="Ahamd", middle_name="A B C", last_name="Alahmadi", password="itsahim")

		self.group = Group.objects.create(name='student')
		self.instructor_group = Group.objects.create(name='instructor')

		now = datetime.now()

		self.user.groups.add(Group.objects.get(name='student'))
		self.user2.groups.add(Group.objects.get(name='instructor'))

		self.semester = Semester.objects.create(year=2021, semester=2, registration_starts=now - timedelta(days=10), registration_ends=now + timedelta(days=30), grading_deadline=now + timedelta(days=90), exams_starts=now + timedelta(days=80), exams_ends=now + timedelta(days=88), semester_starts = now + timedelta(days=30), semester_ends=now + timedelta(days=90), status=1)

		self.student = Student.objects.create(login = self.user, sex = "M", passed_terms=3, registration_id="2111111", semester = self.semester ,status=1)
		self.instructor = Instructor.objects.create(login = self.user2, registration_id="2111110", dept=self.department)

	
	def tearDown(self):
		self.browser.close()

	def test_inst_sign_in(self):
		self.browser.get(self.live_server_url)

		alert1 = self.browser.find_element_by_id('email')
		alert2 = self.browser.find_element_by_id('password')

		alert1.send_keys('test@instructor.com')
		alert2.send_keys('itsahim')

		self.browser.find_element_by_id('submit').click()

		instructor_homepage_url = self.live_server_url + reverse('portal:instructors_homepage')

		self.assertEquals(
			self.browser.current_url,
			instructor_homepage_url
		)

	def test_show_list(self):
		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		section = Section.objects.create(course=course, snumber='01A', semester=self.semester, days='135', start_time='11:00', end_time='11:50')
		section2 = Section.objects.create(course=course, snumber='02A', semester=self.semester, days='24', start_time='11:00', end_time='11:50')

		self.user2.instructor.section_set.add(section)
		self.user2.instructor.section_set.add(section2)

		self.user.student.section_set.add(section)

		self.browser.get(self.live_server_url)

		alert1 = self.browser.find_element_by_id('email')
		alert2 = self.browser.find_element_by_id('password')

		alert1.send_keys('test@instructor.com')
		alert2.send_keys('itsahim')

		self.browser.find_element_by_id('submit').click()

		instructor_homepage_url = self.live_server_url + reverse('portal:instructors_homepage')

		self.assertEquals(
			self.browser.current_url,
			instructor_homepage_url
		)

		self.browser.find_element_by_link_text('My Sections').click()

		self.assertEquals(
			self.browser.current_url,
			self.live_server_url + reverse('portal:show_sections_list')
		)

		self.browser.find_element_by_id('btn-show-0').click()
		time.sleep(1)

		try:
			self.browser.find_element_by_class_name('btn-hide')
		except:
			self.fail('section list was not shown')
		
	def test_grading(self):
		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		section = Section.objects.create(course=course, snumber='01A', semester=self.semester, days='135', start_time='11:00', end_time='11:50')
		section2 = Section.objects.create(course=course, snumber='02A', semester=self.semester, days='24', start_time='11:00', end_time='11:50')

		self.user2.instructor.section_set.add(section)
		self.user2.instructor.section_set.add(section2)

		self.user.student.section_set.add(section)

		self.browser.get(self.live_server_url)

		alert1 = self.browser.find_element_by_id('email')
		alert2 = self.browser.find_element_by_id('password')

		alert1.send_keys('test@instructor.com')
		alert2.send_keys('itsahim')

		self.browser.find_element_by_id('submit').click()

		instructor_homepage_url = self.live_server_url + reverse('portal:instructors_homepage')

		self.assertEquals(
			self.browser.current_url,
			instructor_homepage_url
		)

		self.browser.find_element_by_link_text('Grade').click()

		self.assertEquals(
			self.browser.current_url,
			self.live_server_url + reverse('portal:grading')
		)

		self.browser.find_element_by_id('btn-show-0').click()
		time.sleep(1)

		try:
			self.browser.find_element_by_class_name('btn-hide')
		except:
			self.fail('section list was not shown')

		stu = self.browser.find_element_by_id('2111111')
		stu.send_keys('A')

		self.browser.find_element_by_class_name('btn-hide').click()
		time.sleep(1)
		try:
			self.browser.switch_to.alert.accept()
		except:
			self.browser.switch_to.alert.accept()

		self.assertEquals(self.user.student.studentsection_set.first().grade, 'A')

	def test_account_page_failed(self):
		self.browser.get(self.live_server_url)

		alert1 = self.browser.find_element_by_id('email')
		alert2 = self.browser.find_element_by_id('password')

		alert1.send_keys('test@instructor.com')
		alert2.send_keys('itsahim')

		self.browser.find_element_by_id('submit').click()

		instructor_homepage_url = self.live_server_url + reverse('portal:instructors_homepage')

		self.assertEquals(
			self.browser.current_url,
			instructor_homepage_url
		)

		self.browser.find_element_by_link_text('Account').click()

		self.assertEquals(
			self.browser.current_url,
			self.live_server_url + reverse('portal:instructor_account')
		)

		old_password = self.browser.find_element_by_id('old_password').send_keys('itsahim')
		new_password = self.browser.find_element_by_id('new_password').send_keys('itsaus')
		confirm_password = self.browser.find_element_by_id('con_password').send_keys('itsaus')

		self.browser.find_element_by_id('change-btn').click()

		try:
			self.browser.find_element_by_class_name('text-red-500')
		except:
			self.fail('password authentication failed')
		

	def test_account_page(self):
		self.browser.get(self.live_server_url)

		password = self.user2.password
	
		alert1 = self.browser.find_element_by_id('email')
		alert2 = self.browser.find_element_by_id('password')

		alert1.send_keys('test@instructor.com')
		alert2.send_keys('itsahim')

		self.browser.find_element_by_id('submit').click()

		instructor_homepage_url = self.live_server_url + reverse('portal:instructors_homepage')

		self.assertEquals(
			self.browser.current_url,
			instructor_homepage_url
		)

		self.browser.find_element_by_link_text('Account').click()

		self.assertEquals(
			self.browser.current_url,
			self.live_server_url + reverse('portal:instructor_account')
		)

		old_password = self.browser.find_element_by_id('old_password').send_keys('itsahim')
		new_password = self.browser.find_element_by_id('new_password').send_keys('itsaUS$@1')
		confirm_password = self.browser.find_element_by_id('con_password').send_keys('itsaUS$@1')

		self.browser.find_element_by_id('change-btn').click()

		try:
			login = Login.objects.get(email='test@instructor.com')
		except:
			self.fail('Error getting Login data')

		self.assertNotEquals(login.password, password)
