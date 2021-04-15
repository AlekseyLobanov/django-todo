from api import User


def ignore_exceptions(*args, **argv):
    try:
        args[0](*(args[1:]), **argv)
    except Exception as e:
        print(e)


user = User()
print("testing api methods...")
print("auth..."), ignore_exceptions(user.auth, "root", "root")
print("list..."), ignore_exceptions(user.list)
print("create..."), ignore_exceptions(user.create)
print("read..."), ignore_exceptions(user.read, id=0)
print("update..."), ignore_exceptions(user.update, id=0, title="Title")
print("partial_update..."), ignore_exceptions(user.partial_update, id=0, title="Title")
print("delete..."), ignore_exceptions(user.update, id=0)
