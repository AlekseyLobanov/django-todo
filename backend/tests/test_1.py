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

    def delete(self, id):
        url_with_id = reverse('ToDoLists-detail', args=(id,))
        response = self.client.delete(url_with_id, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_todo(self):
        """
        lists/: get, post
        lists/{id}/: get, put (update), patch (partial_update), delete
        """

        user = User.objects.create_user('test_user', 'test@test.com', 'test_password')
        self.client.force_authenticate(user=user)

        self.get([])
        to_do_title_1, to_do_title_2 = "ToDoList1", "ToDoList2"
        to_do_id1 = self.post(to_do_title_1)
        self.get([to_do_title_1])
        to_do_id2 = self.post(to_do_title_2)
        self.get([to_do_title_1, to_do_title_2])

        self.get_by_id(to_do_id1, to_do_title_1)
        self.get_by_id(to_do_id2, to_do_title_2)

        self.delete(to_do_id2)
        self.get([to_do_title_1])

        self.put(to_do_id1, "ToDoList11")

        self.patch(to_do_id1, "ToDoList12")
        
class ItemTest(APITestCase):
    '''Tests API for items.'''
    def get(self, todo_id, finished, expected_titles):
        url = reverse('ToDoItems-list')
        if finished is not None:
            data = {"parent": todo_id, "finished": finished}
        else:
            data = {"parent": todo_id}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        real_titles = [d['text'] for d in response.data['results']]
        self.assertEqual((response.data['count'], real_titles), \
            (len(expected_titles), expected_titles))

        if finished is not None:
            item_status = [data['finished'] for data in response.data['results']]
            self.assertEqual(finished, all(item_status))

    def post(self, item_text, todo_id, finished):
        url = reverse('ToDoItems-list')
        if finished is not None:
            data = {"text": item_text, "parent": todo_id, "finished": finished}
        else:
            data = {"text": item_text, "parent": todo_id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        check_finished = False if (finished is None) else finished
        self.assertEqual((response.data['text'], response.data['parent'], response.data['finished']), \
            (item_text, todo_id, check_finished))
        return response.data['id']

    def delete(self, id):
        url_with_id = reverse('ToDoItems-detail', args=(id,))
        response = self.client.delete(url_with_id, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_items(self):
        """
        /todo_items/: get+, post+ (create)
        /todo_items/{id}/: get (read), put (update), patch (partial_update), delete+
        """
        user = User.objects.create_user('test_user', 'test@test.com', 'test_password')
        self.client.force_authenticate(user=user)
        to_do_id = create_todo(self.client, "ToDoList").data['id']
        self.get(to_do_id, None, [])
        item_id_1 = self.post("Item1", to_do_id, None)
        self.get(to_do_id, None, ["Item1"])
        item_id_2 = self.post("Item2", to_do_id, False)
        self.get(to_do_id, None, ["Item1", "Item2"])
        item_id_3 = self.post("Item3", to_do_id, True)
        self.get(to_do_id, None, ["Item1", "Item2", "Item3"])
        self.get(to_do_id, False, ["Item1", "Item2"])
        self.get(to_do_id, True, ["Item3"])

        self.delete(item_id_3)
        self.get(to_do_id, None, ["Item1", "Item2"])


