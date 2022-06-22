from selenium import webdriver
from portal.models import *
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
from datetime import datetime, timedelta

class TestSkyedStudent(StaticLiveServerTestCase):
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
		self.semester = Semester.objects.create(year=2021, semester=2, registration_starts=now - timedelta(days=10), registration_ends=now + timedelta(days=30), grading_deadline=now + timedelta(days=90), exams_starts=now + timedelta(days=80), exams_ends=now + timedelta(days=88), semester_starts = now + timedelta(days=30), semester_ends=now + timedelta(days=90), status=1)

		self.student = Student.objects.create(login = self.user, sex = "M", passed_terms=3, registration_id="2111111", semester = self.semester ,status=1)
		self.instructor = Instructor.objects.create(login = self.user2, registration_id="2111110", dept=self.department)

	def tearDown(self):
		self.browser.close()

	def test_invalid_user(self):
		self.browser.get(self.live_server_url)

		alert1 = self.browser.find_element_by_id('email')
		alert2 = self.browser.find_element_by_id('password')

		alert1.send_keys('test@student.com')
		alert2.send_keys('itsahim')

		self.browser.find_element_by_id('submit').click()

		login_page = self.live_server_url + reverse('portal:login_view')

		self.assertEquals(
			self.browser.current_url,
			login_page
		)


	def test_sign_in(self):
		self.browser.get(self.live_server_url)

		alert1 = self.browser.find_element_by_id('email')
		alert2 = self.browser.find_element_by_id('password')

		alert1.send_keys('test@student.com')
		alert2.send_keys('itsame')

		self.browser.find_element_by_id('submit').click()

		student_homepage_url = self.live_server_url + reverse('portal:student_homepage')

		self.assertEquals(
			self.browser.current_url,
			student_homepage_url
		)
	
	def test_registration_not_period(self):
		self.semester.registration_starts = datetime.now() + timedelta(days=7)
		print(self.semester.registration_starts)
		self.semester.save()

		self.browser.get(self.live_server_url)

		alert1 = self.browser.find_element_by_id('email')
		alert2 = self.browser.find_element_by_id('password')

		alert1.send_keys('test@student.com')
		alert2.send_keys('itsame')

		self.browser.find_element_by_id('submit').click()

		student_homepage_url = self.live_server_url + reverse('portal:student_homepage')

		self.assertEquals(
			self.browser.current_url,
			student_homepage_url
		)

		self.browser.find_element_by_link_text('Registration').click()

		registration_url = self.live_server_url + reverse('portal:registration_view')

		self.assertEquals(self.browser.current_url, registration_url)
		
		try:
			self.browser.find_element_by_id('not_register_time')
		except:
			self.fail('The Student is not supposed to be allowed to register')


	def test_registration_and_planner(self):
		course = Course.objects.create(course_id="0418141", course_name="Programming 1", credits=4, department=self.department)

		section = Section.objects.create(course=course, snumber='01A', semester=self.semester, days='135', start_time='11:00', end_time='11:50')
		section2 = Section.objects.create(course=course, snumber='02A', semester=self.semester, days='24', start_time='11:00', end_time='11:50')

		self.browser.get(self.live_server_url)

		alert1 = self.browser.find_element_by_id('email')
		alert2 = self.browser.find_element_by_id('password')

		alert1.send_keys('test@student.com')
		alert2.send_keys('itsame')

		self.browser.find_element_by_id('submit').click()

		student_homepage_url = self.live_server_url + reverse('portal:student_homepage')

		self.assertEquals(
			self.browser.current_url,
			student_homepage_url
		)

		self.browser.find_element_by_link_text('Registration').click()

		registration_url = self.live_server_url + reverse('portal:registration_view')

		self.assertEquals(self.browser.current_url, registration_url)
		self.browser.find_element_by_link_text('Change registration plan').click()

		self.assertEquals(self.browser.current_url, self.live_server_url + reverse('portal:planner_view'))

		try:
			self.browser.find_element_by_id('search-box').send_keys('programming')
		except:
			self.fail('Error when using the search bar')
		
		try:
			self.browser.find_element_by_class_name('search-btn').click()
		except:
			self.fail('Error When Clicking the search button')

		time.sleep(1)
		try:
			self.browser.find_element_by_id('0418141').click()
		except:
			self.fail('Error When adding to the planner')

		time.sleep(1)
		try:
			self.browser.switch_to.alert.accept()
		except:
			self.browser.switch_to.alert.accept()

		try:
			added_course = Course.objects.get(course_id='0418141')
		except:
			self.fail('Course Not Found')
		
		self.browser.find_element_by_link_text('Registration').click()

		self.assertEquals(self.browser.current_url, registration_url)

		self.browser.find_element_by_id('0418141').click()
		time.sleep(1)

		sec = self.browser.find_element_by_class_name('sec-add-btn').click()
		time.sleep(1)

		try:
			section = self.user.student.section_set.get(course__course_id='0418141')
		except:
			self.fail("section wasn't added")

	def test_issue_towhom(self):
		self.browser.get(self.live_server_url)

		alert1 = self.browser.find_element_by_id('email')
		alert2 = self.browser.find_element_by_id('password')

		alert1.send_keys('test@student.com')
		alert2.send_keys('itsame')

		self.browser.find_element_by_id('submit').click()

		student_homepage_url = self.live_server_url + reverse('portal:student_homepage')

		self.assertEquals(
			self.browser.current_url,
			student_homepage_url
		)

		self.browser.find_element_by_link_text('Account').click()

		self.assertEquals(self.browser.current_url, self.live_server_url + reverse('portal:account_view'))
	
		self.browser.find_element_by_name('towhom').click()
		doc = Document.objects.first()

		self.assertEquals(self.browser.current_url, self.live_server_url + reverse('portal:show_document', args=[doc.id]))