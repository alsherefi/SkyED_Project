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



class TestDocumentView(APITestCase):
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


	def test_create_document_POST_doc_doesnt_exist(self):
		self.client.login(email="test@student.com", password="123kdcow")

		response = self.client.post(reverse('portal:create_document', args=[3]))

		self.assertEquals(response.status_code, 404)

	def test_create_towhom_POST(self):
		self.client.login(email="test@student.com", password="123kdcow")

		response = self.client.post(reverse('portal:create_document', args=[1]))

		self.assertEquals(response.status_code, 302)

	def test_create_transcript_view(self):
		self.client.login(email="test@student.com", password="123kdcow")

		response = self.client.post(reverse('portal:create_document', args=[2]))

		self.assertEquals(response.status_code, 302)


	def show_towhom_GET(self):
		doc = Document.objects.create(login=self.user, doc_type=1, semester=self.semester)

		response = self.client.get(reverse('portal:show_document', args=[doc.id]))

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed("portal/student/show_document.html")
		self.assertEquals(response.context['document'].id, doc.id)

	def show_towhom_GET_wrong_type(self):
		doc = Document.objects.create(login=self.user, doc_type=2, semester=self.semester)

		response = self.client.get(reverse('portal:show_document', args=[doc.id]))

		self.assertEquals(response.status_code, 404)

	def show_towhom_GET_dose_not_exist(self):
		response = self.client.get(reverse('portal:show_document', args=['d3b148d3-087c-4271-99e0-465fbcd1634e']))

		self.assertEquals(response.status_code, 404)

	def show_transcript_GET(self):
		doc = Document.objects.create(login=self.user, doc_type=2, semester=self.semester)

		response = self.client.get(reverse('portal:show_transcript', args=[doc.id]))

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed("portal/student/transcript.html")
		self.assertEquals(response.context['document'].id, doc.id)

	def show_transcript_GET_wrong_type(self):
		doc = Document.objects.create(login=self.user, doc_type=1, semester=self.semester)

		response = self.client.get(reverse('portal:show_transcript', args=[doc.id]))

		self.assertEquals(response.status_code, 404)

	def show_transcript_GET_dose_not_exist(self):
		response = self.client.get(reverse('portal:show_transcript', args=['d3b148d3-087c-4271-99e0-465fbcd1634e']))

		self.assertEquals(response.status_code, 404)
