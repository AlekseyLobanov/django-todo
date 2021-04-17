from django.db import models
from django.contrib.auth.models import User


class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=None)
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)


class ToDoItem(models.Model):
    parent = models.ForeignKey(ToDoList, on_delete=models.CASCADE, null=False, default=None)
    text = models.TextField()
    finished = models.BooleanField(default=False, null=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
