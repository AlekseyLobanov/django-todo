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

def create_todo(client, title):
    url = reverse('ToDoLists-list')
    response = client.post(url, {"title": title}, format='json')
    return response

class ToDoTest(APITestCase):
    '''Tests API for todo.'''
    def get(self, expected_titles):
        url = reverse('ToDoLists-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        real_titles = [data['title'] for data in response.data['results']]
        self.assertEqual((response.data['count'], real_titles), \
            (len(expected_titles), expected_titles))

    def post(self, to_do_title):
        response = create_todo(self.client, to_do_title)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], to_do_title)
        return response.data['id']

    def get_by_id(self, id, expected_title):
        url_with_id = reverse('ToDoLists-detail', args=(id,))
        response = self.client.get(url_with_id, {id: id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], expected_title)

    def put(self, id, new_title):
        url_with_id = reverse('ToDoLists-detail', args=(id,))
        response = self.client.put(url_with_id, {"title": new_title}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_title)

    def patch(self, id, new_title):
        url_with_id = reverse('ToDoLists-detail', args=(id,))
        response = self.client.patch(url_with_id, {"title": new_title}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_title)

    def delete(self, id, title):
        self.get_by_id(id, title)
        url_with_id = reverse('ToDoLists-detail', args=(id,))
        response = self.client.delete(url_with_id, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def prepare(self):
        user = User.objects.create_user('test_user', 'test@test.com', 'test_password')
        self.client.force_authenticate(user=user)

    def test_create_delete(self):
        """
        lists/{id}/: put (update), patch (partial_update)
        """
        self.prepare()
        to_do_title_1 = "ToDoList1"
        to_do_id1 = self.post(to_do_title_1)
        self.put(to_do_id1, "ToDoList11")
        self.patch(to_do_id1, "ToDoList12")


    def test_todo(self):
        """
        lists/: get, post
        lists/{id}/: get, delete
        """

        self.prepare()
        self.get([])
        to_do_title_1, to_do_title_2 = "ToDoList1", "ToDoList2"
        to_do_id1 = self.post(to_do_title_1)
        self.get([to_do_title_1])
        to_do_id2 = self.post(to_do_title_2)
        self.get([to_do_title_1, to_do_title_2])

        self.get_by_id(to_do_id1, to_do_title_1)
        self.get_by_id(to_do_id2, to_do_title_2)

        self.delete(to_do_id2, to_do_title_2)
        self.get([to_do_title_1])

