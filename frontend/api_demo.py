from api import User, CODE_SUCCESS

user = User()
print("testing api methods...")
print("auth...", user.auth("root", "root") == CODE_SUCCESS)
print("list...", user.list()[0] == CODE_SUCCESS)
print("create...", user.create()[0] == CODE_SUCCESS)
print("read...", user.read(id=0)[0] == CODE_SUCCESS)
print("update...", user.update(id=0, title="Title")[0] == CODE_SUCCESS)
print("partial_update...", user.partial_update(id=0, title="Title")[0] == CODE_SUCCESS)
print("delete...", user.update(id=0)[0] == CODE_SUCCESS)