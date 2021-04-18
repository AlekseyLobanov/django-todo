import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from backend.api import router

class EasyTest(APITestCase):
    def test_list(self):
        """
        The first test.
        """
        user = User.objects.create_user('test_user', 'test@test.com', 'test_password')

        url = reverse('ToDoLists-list')#reverse('ToDoLists-list')
        data = {}
        self.client.force_authenticate(user=user)
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])