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
from collections import OrderedDict

class EasyTest(APITestCase):

    def test_list(self):
        """
        The first test.
        """
        user = User.objects.create_user('test_user', 'test@test.com', 'test_password')
        url = reverse('ToDoLists-list')
        self.client.force_authenticate(user=user)

        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, OrderedDict([('count', 0), ('next', None), ('previous', None), ('results', [])]))
    
        response = self.client.post(url, {"title": "ToDoList1"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "ToDoList1")

        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual((response.data['count'], response.data['next'], response.data['previous'], \
            response.data['results'][0]['title']), (1, None, None, "ToDoList1"))