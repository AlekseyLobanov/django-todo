#!usr/bin/env python3
'''
'''

import glob

def task_wheel():
    """Create bynary wheel distribution"""
    return {
        'actions': ['python3 -m build -w']
    }
