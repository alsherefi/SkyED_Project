from django.test import TestCase, Client

import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import *
from datetime import datetime, timedelta

from django.contrib.auth import login, authenticate, logout

class TestIndexView(APITestCase):
	def test_homepage_GET(self):
		client = Client()
		response = client.get(reverse('portal:login_view'))


		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'portal/index.html')
