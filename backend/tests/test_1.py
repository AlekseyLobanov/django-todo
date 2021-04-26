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

class EasyTest1(APITestCase):
    def get_todo(self, expected_titles):
        response = self.client.get(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        real_titles = [data['title'] for data in response.data['results']]
        self.assertEqual((response.data['count'], real_titles), \
            (len(expected_titles), expected_titles))

    def post_todo(self, to_do_title):
        response = self.client.post(self.url, {"title": to_do_title}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], to_do_title)
        return response.data['id']

    def get_todo_by_id(self, id, expected_title):
        url_with_id = reverse('ToDoLists-detail', args=(id,))
        response = self.client.get(url_with_id, {id: id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], expected_title)

    def put_todo(self, id, new_title):
        url_with_id = reverse('ToDoLists-detail', args=(id,))
        response = self.client.put(url_with_id, {"title": new_title}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_title)

    def patch_todo(self, id, new_title):
        url_with_id = reverse('ToDoLists-detail', args=(id,))
        response = self.client.patch(url_with_id, {"title": new_title}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_title)

    def delete_todo(self, id):
        url_with_id = reverse('ToDoLists-detail', args=(id,))
        response = self.client.delete(url_with_id, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_todo(self):
        """
        Tests API for todo.

        lists/: get, post
        lists/{id}/: get, put (update), patch (partial_update), delete
        """

        user = User.objects.create_user('test_user', 'test@test.com', 'test_password')
        self.client.force_authenticate(user=user)
        self.url = reverse('ToDoLists-list')

        self.get_todo([])
        to_do_title_1, to_do_title_2 = "ToDoList1", "ToDoList2"
        to_do_id1 = self.post_todo(to_do_title_1)
        self.get_todo([to_do_title_1])
        to_do_id2 = self.post_todo(to_do_title_2)
        self.get_todo([to_do_title_1, to_do_title_2])

        self.get_todo_by_id(to_do_id1, to_do_title_1)
        self.get_todo_by_id(to_do_id2, to_do_title_2)

        self.delete_todo(to_do_id2)
        self.get_todo([to_do_title_1])

        self.put_todo(to_do_id1, "ToDoList11")

        self.patch_todo(to_do_id1, "ToDoList12")
        