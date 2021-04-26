from types import SimpleNamespace
import urllib
import requests

DEFAULT_URL = "http://127.0.0.1:8000"

API_TODO_ITEMS_LIST = "api/todo_items/"
API_TODO_ITEMS_CREATE = "api/todo_items/"
API_TODO_ITEMS_READ = "api/todo_items/{0}/"
API_TODO_ITEMS_UPDATE = "api/todo_items/{0}/"
API_TODO_ITEMS_PARTIAL_UPDATE = "api/todo_items/{0}/"
API_TODO_ITEMS_DELETE = "api/todo_items/{0}/"

API_LISTS_LIST = "api/lists/"
API_LISTS_CREATE = "api/lists/"
API_LISTS_READ = "api/lists/{0}/"
API_LISTS_UPDATE = "api/lists/{0}/"
API_LISTS_PARTIAL_UPDATE = "api/lists/{0}/"
API_LISTS_DELETE = "api/lists/{0}/"

API_TOKEN = "api/token/"


class UserApi(object):
    def __init__(self, url=DEFAULT_URL, token=None):
        """
        Constructor

        Parameters
        ----------
        url : str, optional
            Server url. The default is DEFAULT_URL.
        token : dict, optional
            Existing user tokens to bypass authorization.
            The default is None.

        Returns
        -------
        None.

        """
        self.token = token
        self.get_api = lambda x: urllib.parse.urljoin(url, x)

    # ToDo - store tokens in config
    def auth(self, user, passwd):
        """
        Authosization

        Parameters
        ----------
        user : str
            Login.
        passwd : str
            Password.

        Returns
        -------
        dict
            Generated auth token.

        """
        token = UserApi._raise_or_return_(
            requests.post(url=self.get_api(API_TOKEN), json={"username": user, "password": passwd})
        )
        self.token = SimpleNamespace(**token)
        return self.token

    def lists_list(self, **argv):
        """
        List all the exsiting to-do lists.
        Auth required

        Returns
        -------
        list
            to-do lists.

        """
        return UserApi._raise_or_return_(
            requests.get(
                url=self.get_api(API_LISTS_LIST), headers=self._access_token_(), params=argv
            )
        )

    def lists_create(self, title="Untitled"):
        """
        Create a new to-do list
        Auth required

        Parameters
        ----------
        title : str, optional
            New list name. The default is "Untitled".

        """
        return UserApi._raise_or_return_(
            requests.post(
                url=self.get_api(API_LISTS_CREATE),
                json={"title": title},
                headers=self._access_token_(),
            )
        )

    def lists_delete(self, id):
        """
        Auth required

        Deletes a to-do list by id

        Parameters
        ----------
        id: to-do list id to delete
        """
        return UserApi._raise_or_return_(
            requests.delete(
                url=self.get_api(API_LISTS_DELETE.format(id)),
                headers=self._access_token_(),
            )
        )

    def lists_update(self, title, id):
        """
        Rename a new to-do list
        Auth required

        Parameters
        ----------
        title : str
            New name for a list.
        id : int

        """
        return UserApi._raise_or_return_(
            requests.put(
                url=self.get_api(API_LISTS_UPDATE.format(id)),
                json={"title": title},
                headers=self._access_token_(),
            )
        )

    def todo_items_list(self, **argv):
        """
        List all the exsiting to-do items.
        Auth required

        Returns
        -------
        list
            to-do items.

        """
        return UserApi._raise_or_return_(
            requests.get(
                url=self.get_api(API_TODO_ITEMS_LIST), headers=self._access_token_(), params=argv
            )
        )

    def todo_items_create(self, parent, text="Note"):
        """
        Create a new to-do item
        Auth required

        Parameters
        ----------
        parent : id of parent list
        text : str, optional
            New note. The default is "Note".

        """
        return UserApi._raise_or_return_(
            requests.post(
                url=self.get_api(API_TODO_ITEMS_CREATE),
                json={"text": text, "parent": parent, "finished": False},
                headers=self._access_token_(),
            )
        )

    def todo_items_delete(self, id):
        """
        Auth required

        Deletes a to-do item by id

        Parameters
        ----------
        id: to-do item id to delete
        """
        return UserApi._raise_or_return_(
            requests.delete(
                url=self.get_api(API_TODO_ITEMS_DELETE.format(id)),
                headers=self._access_token_(),
            )
        )

    def todo_items_update(self, id, text, finished, parent):
        """
        Rename a new to-do list
        Auth required

        Parameters
        ----------
        id : int
            Note id
        text : str
            New note for the item.
        finished : bool
            New state for the item
        parent : int
            Parent list id
        """
        return UserApi._raise_or_return_(
            requests.put(
                url=self.get_api(API_TODO_ITEMS_UPDATE.format(id)),
                json={"text": text, "finished": finished, "parent": parent},
                headers=self._access_token_(),
            )
        )

    # def create(self, title="Untitled"):
    # """
    # Create a new to-do list
    # Auth required

    # Parameters
    # ----------
    # title : str, optional
    # New list name. The default is "Untitled".

    # """
    # response = requests.post(
    # url=self.get_api(API_LISTS_CREATE), json={"title": title}, headers=self._access_token_()
    # url=self.get_api(API_TODO_ITEMS_CREATE), json={"title": title}, headers=self._access_token_()
    # )
    # response.raise_for_status()
    # return response.json()

    # def read(self, id):
    # """
    # Read a to-do list contents

    # Parameters
    # ----------
    # id : int
    # List id.

    # Returns
    # -------
    # list
    # Requested contents

    # """
    # response = requests.post(
    # url=self.get_api(API_LISTS_READ).format(id), headers=self._access_token_()
    # )
    # response.raise_for_status()
    # return response.json()

    # def update(self, id, title="Untitled"):
    # """
    # Add a to-do item to the list

    # Parameters
    # ----------
    # id : int
    # List id.
    # title : str, optional
    # To-do item title. The default is "Untitled".

    # """
    # response = requests.put(
    # json={"title": title},
    # url=self.get_api(API_LISTS_UPDATE).format(id),
    # headers=self._access_token_(),
    # )
    # response.raise_for_status()
    # return response.json()

    # def partial_update(self, id, title="Untitled"):
    # """
    # Update list item - untrusted

    # """
    # response = requests.patch(
    # json={"title": title},
    # url=self.get_api(API_LISTS_PARTIAL_UPDATE).format(id),
    # headers=self._access_token_(),
    # )
    # response.raise_for_status()
    # return response.json()

    # def delete(self, id):
    # """
    # Delete list

    # Parameters
    # ----------
    # id : int
    # List id to delete.

    # """
    # response = requests.delete(
    # url=self.get_api(API_LISTS_DELETE).format(id), headers=self._access_token_()
    # )
    # response.raise_for_status()
    # return response.json()

    def _access_token_(self):
        if self.token is None:
            raise RuntimeError("Authosization required for requested operation!")
        return {"Authorization": f"Bearer {self.token.access}"}

    @staticmethod
    def _raise_or_return_(response):
        response.raise_for_status()
        try:
            return response.json()
        except Exception as e:
            print(e)
            return response.content
