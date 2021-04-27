import os
import random
from datetime import datetime
from types import SimpleNamespace

from pathlib import Path

import json

from api import UserApi

LIST_UPDATEBLE = ["title"]
TODO_ITEM_UPDATEBLE = ["text", "finished"]
UPDATE_ERROR = "Failed to update property: {0}"

DATETIME_STR = "%Y-%m-%dT%H:%M:%S.%fZ"

USER_TOKEN_PATH = os.path.join(Path.home(), ".todo_config.json")


def bad_arguments(x, d):
    return list((set(x) - set(d)))


def date_or_str(inpt):
    if type(inpt) is datetime:
        return inpt
    elif type(inpt) is str:
        return datetime.strptime(inpt, DATETIME_STR)
    else:
        return datetime.now()


class ToDoList(object):
    def __init__(self, id, title, created_at=None, items=None, parent=None, user=None):
        self.id = id
        self.title = title
        self.items_ = [] if items is None else items
        self.created_at = date_or_str(created_at)
        self.user = user

    def __iter__(self):
        for item in self.items_:
            yield item

    def __getitem__(self, index):
        return self.items_[index]

    def __len__(self):
        return len(self.items_)

    def __str__(self):
        return f"[{self.id}] {self.title}"

    def index(self, value):
        return self.items_.index(value)

    def remove(self, index):
        """
        Remove item at index from db
        """
        item = self.items_[index]
        self.items_.remove(item)
        item.dispose()

    def append(self, text):
        """
        Add a new item to db
        """
        if "DEBUG" in os.environ:
            created_item = ToDoItem(id=random.randint(100, 1000), text=text, user=self.user)
        else:
            created_item = self.user.todo_items_create(parent=self.id, text=text)
            created_item = ToDoItem(**created_item, user=self.user)
        self.items_.append(created_item)
        return created_item

    def modify(self, **argv):
        bad = bad_arguments(argv.keys(), LIST_UPDATEBLE)
        if len(bad) > 0:
            raise RuntimeError(UPDATE_ERROR.format(bad[0]))
        for key, value in argv.items():
            setattr(self, key, value)
        self.sync()

    def dispose(self):
        print(f"To-do list id '{self.id}' is being disposed of...")
        if "DEBUG" in os.environ:
            return
        for item in self.items_:
            item.dispose()
        self.user.lists_delete(self.id)

    def sync(self):
        print(f"Item '{self}' is being synchronized...")
        if "DEBUG" in os.environ:
            return
        self.user.lists_update(title=self.title, id=self.id)


class ToDoItem(object):
    def __init__(self, id, text, finished=False, created_at=None, parent=None, user=None):
        self.id = id
        self.text = text
        self.finished = finished
        self.created_at = date_or_str(created_at)
        self.parent = parent
        self.user = user

    def __str__(self):
        return f"[{self.id}] {self.text}"

    def modify(self, **argv):
        bad = bad_arguments(argv.keys(), TODO_ITEM_UPDATEBLE)
        if len(bad) > 0:
            raise RuntimeError(UPDATE_ERROR.format(bad[0]))
        for key, value in argv.items():
            setattr(self, key, value)
        self.sync()

    def dispose(self):
        print(f"To-do item id '{self.id}' is being disposed of...")
        if "DEBUG" in os.environ:
            return
        self.user.todo_items_delete(self.id)

    def sync(self):
        print(f"Item '{self}' is being synchronized...")
        if "DEBUG" in os.environ:
            return
        self.user.todo_items_update(
            id=self.id, text=self.text, finished=self.finished, parent=self.parent
        )


def make_debug_lists():
    return [
        ToDoList(
            id=i,
            title=f"List {i}",
            created_at=datetime.now(),
            items=[
                ToDoItem(id=i * 10 + j, text=f"Item {i*10+j}", created_at=datetime.now())
                for j in range(10)
            ],
        )
        for i in range(10)
    ]


class User(UserApi):
    def auth(self, user, passwd):
        """
        Basic authentification
        """
        if "DEBUG" in os.environ:
            return
        return UserApi.auth(self, user, passwd)

    def remove(self):
        """
        Remove the login file from homedir
        """
        if not os.path.exists(USER_TOKEN_PATH):
            return
        try:
            os.remove(USER_TOKEN_PATH)
        except Exception as e:
            raise RuntimeError("Failed to remove tokens:", e)

    def save(self):
        """
        Store user token in homedir
        """
        try:
            with open(USER_TOKEN_PATH, "w") as handler:
                json.dump(self.token.__dict__, handler)
        except Exception as e:
            raise RuntimeError("Failed to store tokens:", e)

    @staticmethod
    def load():
        """
        Restore user token from the file in homedir
        """
        if os.path.exists(USER_TOKEN_PATH):
            try:
                with open(USER_TOKEN_PATH, "r") as handler:
                    user = User(token=SimpleNamespace(**json.load(handler)))
                    user.refresh()
                    return user
            except Exception as e:
                raise RuntimeError("Failed to restore tokens:", e)
        return None

    # Storing lists - mostly for debug purposes
    lists_ = make_debug_lists()

    def fetchUserLists(self):
        """
        Fetch existing user lists from the server
        returns: fetched list of ToDoList sorted by creation datetime
        """
        print("Fetching lists...")
        if "DEBUG" in os.environ:
            return self.lists_
        user_lists = self.lists_list()["results"]
        user_items = self.todo_items_list()["results"]
        todo_lists = {x["id"]: ToDoList(**x, user=self) for x in user_lists}
        todo_items = [ToDoItem(**x, user=self) for x in user_items]
        for todo_item in todo_items:
            # Catching stray items
            # if not hasattr(toDoItem, "parent"):
            #    toDoItem.dispose()
            #    continue
            todo_lists[todo_item.parent].items_.append(todo_item)
        for todo_list in todo_lists.values():
            todo_list.items_ = sorted(todo_list.items_, key=lambda x: x.created_at)
        self.lists_ = sorted(todo_lists.values(), key=lambda x: x.created_at)
        return self.lists_

    def removeUserList(self, id):
        """
        Remove existing user to-do list from the serverreturns:
        """
        to_remove = [item for item in self.lists_ if item.id == id][0]
        self.lists_.remove(to_remove)
        if not ("DEBUG" in os.environ):
            to_remove.dispose()
        return self.lists_

    def appendUserList(self, title):
        """
        Create a new user list
        title: title of list to create
        returns: created item
        """
        if "DEBUG" in os.environ:
            item = ToDoList(id=random.randint(100, 1000), title=title, created_at=datetime.now())
            self.lists_.append(item)
            return item
        created_list = self.lists_create(title=title)
        created_list = ToDoList(**created_list)
        return created_list
