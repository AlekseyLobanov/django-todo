from django.contrib import admin

from .models import ToDoList, ToDoItem


class ToDoListAdmin(admin.ModelAdmin):
    model = ToDoList
    list_display = ["user", "title", "created_at"]
    list_editable = ["title"]


class ToDoItemAdmin(admin.ModelAdmin):
    model = ToDoItem
    list_display = ["parent", "finished", "text", "created_at"]
    list_editable = ["finished", "text"]


admin.site.register(ToDoList, ToDoListAdmin)
admin.site.register(ToDoItem, ToDoItemAdmin)
