import urllib
import requests

DEFAULT_URL = "http://127.0.0.1:8000"
API_LISTS_LIST = "api/lists/"
API_LISTS_CREATE = "api/lists/"
API_LISTS_READ = "lists/{0}/"
API_LISTS_UPDATE = "lists/{0}/"
API_LISTS_PARTIAL_UPDATE = "lists/{0}/"
API_LISTS_DELETE = "lists/{0}/"
API_TOKEN = "api/token/"


class User(object):
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
        url = self.get_api(API_TOKEN)
        data = {"username": user, "password": passwd}
        response = requests.post(url=url, json=data)
        response.raise_for_status()
        self.token = response.json()
        return self.token

    def list(self):
        """
        List all the exsiting to-do lists.
        Auth required

        Returns
        -------
        list
            to-do lists.

        """
        response = requests.get(url=self.get_api(API_LISTS_LIST), headers=self._access_token_())
        response.raise_for_status()
        return response.json()

    def create(self, title="Untitled"):
        """
        Create a new to-do list

        Parameters
        ----------
        title : str, optional
            New list name. The default is "Untitled".

        """
        response = requests.post(
            url=self.get_api(API_LISTS_CREATE), json={"title": title}, headers=self._access_token_()
        )
        response.raise_for_status()
        return response.json()

    def read(self, id):
        """
        Read a to-do list contents

        Parameters
        ----------
        id : int
            List id.

        Returns
        -------
        list
            Requested contents

        """
        response = requests.post(
            url=self.get_api(API_LISTS_READ).format(id), headers=self._access_token_()
        )
        response.raise_for_status()
        return response.json()

    def update(self, id, title="Untitled"):
        """
        Add a to-do item to the list

        Parameters
        ----------
        id : int
            List id.
        title : str, optional
            To-do item title. The default is "Untitled".

        """
        response = requests.put(
            json={"title": title},
            url=self.get_api(API_LISTS_UPDATE).format(id),
            headers=self._access_token_(),
        )
        response.raise_for_status()
        return response.json()

    def partial_update(self, id, title="Untitled"):
        """
        Update list item - untrusted

        """
        response = requests.patch(
            json={"title": title},
            url=self.get_api(API_LISTS_PARTIAL_UPDATE).format(id),
            headers=self._access_token_(),
        )
        response.raise_for_status()
        return response.json()

    def delete(self, id):
        """
        Delete list

        Parameters
        ----------
        id : int
            List id to delete.

        """
        response = requests.delete(
            url=self.get_api(API_LISTS_DELETE).format(id), headers=self._access_token_()
        )
        response.raise_for_status()
        return response.json()

    def _access_token_(self):
        if self.token is None:
            raise RuntimeError("Authosization required for requested operation!")
        return {"Authorization": f'Bearer {self.token["access"]}'}
