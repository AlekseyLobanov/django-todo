from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .test_todo import create_todo


class ItemTest(APITestCase):
    """Tests API for items."""

    def prepare(self):
        user = User.objects.create_user("test_user4", "test@test.com", "test_password")
        self.client.force_authenticate(user=user)
        to_do_id_1 = create_todo(self.client, "ToDoList1").data["id"]
        to_do_id_2 = create_todo(self.client, "ToDoList2").data["id"]
        return to_do_id_1, to_do_id_2

    def get(self, expected_titles, todo_id=None, finished=None):
        url = reverse("ToDoItems-list")
        data = {}
        if finished is not None:
            data["finished"] = finished
        if todo_id is not None:
            data["parent"] = todo_id

        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        real_titles = [(d["text"], d["parent"]) for d in response.data["results"]]
        self.assertEqual(real_titles, expected_titles)

        if finished is not None:
            item_status = [data["finished"] for data in response.data["results"]]
            self.assertEqual(finished, all(item_status))

    def post(self, item_text, todo_id, finished=None):
        url = reverse("ToDoItems-list")
        if finished is not None:
            data = {"text": item_text, "parent": todo_id, "finished": finished}
        else:
            data = {"text": item_text, "parent": todo_id}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        check_finished = False if (finished is None) else finished
        self.assertEqual(response.data["text"], item_text)
        self.assertEqual(response.data["parent"], todo_id)
        self.assertEqual(response.data["finished"], check_finished)

        return response.data["id"], response.data["finished"]

    def get_by_id(self, id, text, finished, parent):
        url_with_id = reverse("ToDoItems-detail", args=(id,))
        response = self.client.get(url_with_id, {id: id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], text)
        self.assertEqual(response.data["finished"], finished)
        self.assertEqual(response.data["parent"], parent)

    def put(self, id, text, parent, finished=None):
        url_with_id = reverse("ToDoItems-detail", args=(id,))
        data = {"text": text, "parent": parent}
        if finished is not None:
            data["finished"] = finished
        response = self.client.put(url_with_id, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], text)
        self.assertEqual(response.data["parent"], parent)
        if finished is not None:
            self.assertEqual(response.data["finished"], finished)

    def patch(self, id, text=None, finished=None, parent=None):
        url_with_id = reverse("ToDoItems-detail", args=(id,))
        data = {}
        if text is not None:
            data["text"] = text
        if finished is not None:
            data["finished"] = finished
        if parent is not None:
            data["parent"] = parent
        response = self.client.patch(url_with_id, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if text is not None:
            self.assertEqual(response.data["text"], text)
        if finished is not None:
            self.assertEqual(response.data["finished"], finished)
        if parent is not None:
            self.assertEqual(response.data["parent"], parent)

    def delete(self, id, title, finished, to_do_id):
        self.get_by_id(id, title, finished, to_do_id)
        url_with_id = reverse("ToDoItems-detail", args=(id,))
        response = self.client.delete(url_with_id, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_delete(self):
        """
        /todo_items/: get, post (create)
        /todo_items/{id}/: get (read), delete
        """
        to_do_id_1, to_do_id_2 = self.prepare()
        self.get([], to_do_id_1)
        item_text_1, item_text_2, item_text_3, item_text_4 = "Item1", "Item2", "Item3", "Item4"
        item_id_1, item_finished_1 = self.post(item_text_1, to_do_id_1)
        self.get([(item_text_1, to_do_id_1)], to_do_id_1)
        item_id_2, item_finished_2 = self.post(item_text_2, to_do_id_1, finished=False)
        self.get([(item_text_1, to_do_id_1), (item_text_2, to_do_id_1)], to_do_id_1)
        item_id_3, item_finished_3 = self.post(item_text_3, to_do_id_1, finished=True)
        self.get(
            [(item_text_1, to_do_id_1), (item_text_2, to_do_id_1), (item_text_3, to_do_id_1)],
            to_do_id_1,
        )
        item_id_4, item_finished_4 = self.post(item_text_4, to_do_id_2, finished=False)
        self.get(
            [
                (item_text_1, to_do_id_1),
                (item_text_2, to_do_id_1),
                (item_text_3, to_do_id_1),
                (item_text_4, to_do_id_2),
            ]
        )

        self.get(
            [(item_text_1, to_do_id_1), (item_text_2, to_do_id_1), (item_text_3, to_do_id_1)],
            to_do_id_1,
        )
        self.get([(item_text_1, to_do_id_1), (item_text_2, to_do_id_1)], to_do_id_1, finished=False)
        self.get([(item_text_3, to_do_id_1)], to_do_id_1, finished=True)

        self.get_by_id(item_id_1, item_text_1, item_finished_1, to_do_id_1)
        self.get_by_id(item_id_2, item_text_2, item_finished_2, to_do_id_1)
        self.get_by_id(item_id_3, item_text_3, item_finished_3, to_do_id_1)

        self.delete(item_id_3, item_text_3, item_finished_3, to_do_id_1)
        self.get([(item_text_1, to_do_id_1), (item_text_2, to_do_id_1)], to_do_id_1)

    def test_update(self):
        """
        /todo_items/{id}/: put (update), patch (partial_update)
        """

        to_do_id_1, to_do_id_2 = self.prepare()

        item_text_1 = "Item1"
        item_id_1, item_finished_1 = self.post(item_text_1, to_do_id_1)

        item_text_1_2 = "Item5"
        self.put(item_id_1, item_text_1_2, to_do_id_2)
        self.put(item_id_1, item_text_1_2, to_do_id_2, finished=False)
        self.put(item_id_1, item_text_1_2, to_do_id_2, finished=True)

        item_text_1_3 = "Item6"
        self.patch(item_id_1, parent=to_do_id_1)
        self.patch(item_id_1, finished=True)
        self.patch(item_id_1, text=item_text_1_3)
