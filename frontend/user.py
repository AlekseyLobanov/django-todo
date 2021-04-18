from datetime import datetime
from api import UserApi


class ToDoList(object):
    def __init__(self, id, title, created_at=None, items=[], parent=None):
        self.id = id
        self.title = title
        self.items = items
        self.created_at = created_at

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return f"[{self.id}] {self.title}"

    # ToDo
    def remove(self, index):
        self.items.remove(self.items[0])
        self.sync()

    # ToDo
    def append(self, text):
        item = ToDoItem(id=None, text=text, created_at=datetime.now())
        self.items.append(item)
        item.sync()
        self.sync()
        return item

    def modify(self, **argv):
        for key, value in argv.items():
            setattr(self, key, value)
        self.sync()

    # ToDo
    def sync(self):
        # ToDo send request or store in form
        print(f"Item '{self}' is being synchronized...")


class ToDoItem(object):
    def __init__(self, id, text, finished=False, created_at=None, parent=None):
        self.id = id
        self.text = text
        self.finished = finished
        self.created_at = created_at

    def __str__(self):
        return f"[{self.id}] {self.text}"

    def modify(self, **argv):
        for key, value in argv.items():
            setattr(self, key, value)
        self.sync()

    # ToDo
    def sync(self):
        # ToDo send request or store in form
        print(f"Item '{self}' is being synchronized...")


class User(UserApi):

    # ToDo
    items = [
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

    # ToDo
    def fetchUserLists(self):
        return self.items

    # ToDo
    def removeUserList(self, id):
        self.items = [item for item in self.items if item.id != id]

    # ToDo
    def appendUserList(self, title):
        item = ToDoList(id=None, title=title, created_at=datetime.now())
        self.items.append(item)
        item.sync()
        return item
