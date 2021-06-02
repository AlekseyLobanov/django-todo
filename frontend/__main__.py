#!/usr/bin/env python3
"""django-todo application launcher"""

from .todo_tk import Application

if __name__ == "__main__":
    app = Application()
    app.main(app.login())
