from user import User


def print_lists(lists):
    for item in lists:
        print(f"List: '{item}'", f"Id: {item.id}", "|", "|".join([str(x) for x in item.items]))


DEFAULT_URL = "http://127.0.0.1:8000"

user = User(url=DEFAULT_URL)
user.auth("root", "root")

# Fetch existing lists:
lists = user.fetchUserLists()
print("Fecthing...")
print_lists(lists)

# Remove user list by id:
user.removeUserList(5)
lists = user.fetchUserLists()
print(f"Removing {5}...")
print_lists(lists)

# Append a new list to user:
print("Appending list...")
scroll = user.appendUserList(title="a new list!")
print_lists(lists)

# Modify list 0:
print("Modifyng list...")
lists[0].modify(title="A new title")
print_lists(lists)

# Append item to list:
print("Appending item to last list...")
item = lists[-1].append(text="this is an item")
print_lists(lists)

# Modifying item
print("Modifyng appended item...")
item.modify(finished=True, text="this is an updated item")
print_lists(lists)

# Removing item at 0
print("Removing item 0 from list 0...")
lists[0].remove(0)
print_lists(lists)
