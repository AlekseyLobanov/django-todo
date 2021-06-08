#!usr/bin/env python3
"""
"""


def task_mo():
    """Create bynary wheel distribution"""
    return {
        "actions": [
            """pybabel compile -D todo -i frontend/po/eng/LC_MESSAGES/todo.po -o frontend/po/eng/LC_MESSAGES/todo.mo"""
        ],
        "file_dep": ["frontend/po/eng/LC_MESSAGES/todo.po"],
        "targets": ["frontend/po/eng/LC_MESSAGES/todo.mo"],
    }


def task_wheel():
    """Create bynary wheel distribution"""
    return {"actions": ["python3 -m build -w"], "task_dep": ["mo"]}
