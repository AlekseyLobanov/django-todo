#!usr/bin/env python3
'''
'''

import glob

def task_pot():
    """Create bynary wheel distribution"""
    return {
        'actions': ["""pybabel extract -o todo.pot frontend"""],
        'file_dep': glob.glob('frontend/*.py'),
        'targets': ['todo.pot']
    }

def task_po():
    """Create bynary wheel distribution"""
    return {
        'actions': ["""pybabel update -D todo -d frontend/po -i todo.pot"""],
        'file_dep': ['todo.pot'],
        'targets': ['frontend/po/eng/LC_MESSAGES/todo.po']
    }

def task_mo():
    """Create bynary wheel distribution"""
    return {
        'actions': ["""pybabel compile -D todo -i frontend/po/eng/LC_MESSAGES/todo.po -o frontend/po/eng/LC_MESSAGES/todo.mo"""],
        'file_dep': ['frontend/po/eng/LC_MESSAGES/todo.po'],
        'targets': ['frontend/po/eng/LC_MESSAGES/todo.mo']
    }

def task_wheel():
    """Create bynary wheel distribution"""
    return {
        'actions': ['python3 -m build -w'],
        'task_dep': ['mo']
    }
