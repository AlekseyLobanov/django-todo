from django.contrib import admin

from .models import ToDoList


class ToDoListAdmin(admin.ModelAdmin):
    model = ToDoList
    list_display = ["user", "title", "created_at"]
    list_editable = ["title"]


admin.site.register(ToDoList, ToDoListAdmin)
