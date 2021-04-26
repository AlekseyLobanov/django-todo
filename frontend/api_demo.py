import numpy as np
from user import User


def print_lists(lists):
    for item in lists:
        print(f"List: '{item.title}'", f"Id: {item.id}", "|", "|".join([str(x) for x in item.items_]))


DEFAULT_URL = "http://127.0.0.1:8000"

user = User(url=DEFAULT_URL)
user.auth("root", "root")

# Fetch existing lists:
print_lists(user.fetchUserLists())

# Append a new list to user:
print("Appending list...")
scroll = user.appendUserList(title="a new list!")
print_lists(user.fetchUserLists())

# Remove user list by id:
i = user.lists_[0].id
print(f"Removing {i}...")
user.removeUserList(i)
print_lists(user.fetchUserLists())

# Modify list 0:
print("Modifyng list...")
user.lists_[0].modify(title=f"A new title {np.random.random()}")
print_lists(user.fetchUserLists())

# Append item to list:
print("Appending item to last list...")
item = user.lists_[-1].append(text="this is an item")
print_lists(user.fetchUserLists())

# Modifying item
print("Modifyng appended item...")
item.modify(finished=True, text="this is an updated item")
print_lists(user.fetchUserLists())

# Removing item at 0
print("Removing last item from last list...")
user.lists_[-1].remove(-1)
print_lists(user.fetchUserLists())
