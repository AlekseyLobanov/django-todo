import gettext
import os
import tkinter as tk

gettext.install("todo", os.path.join(os.path.dirname(__file__), "po"))


def str_time(time):
    return time.strftime("%Y-%m-%d %H:%M:%S")


TODO_ITEM_TABLE_TEXT_WIDTH = 25
TODO_ITEM_TABLE_FINISHED_WIDTH = 20

TODO_ITEM_TABLE_CREATED_AT_WIDTH = 25


def placeholder():
    print(_("Не реализовано"))


class ToDoItemWidget(tk.Frame):
    def __init__(self, *args, row_number, item, table, **argv):
        super().__init__(*args, **argv)

        self.parent = self.master
        self.item = item

        self.noteLabel = tk.Label(
            table,
            text=item.text,
            width=TODO_ITEM_TABLE_TEXT_WIDTH,
            justify="center",
            font=("Arial", 8),
        )
        self.noteLabel.grid(row=row_number, column=0)

        self.finished = tk.IntVar(value=int(item.finished))
        self.finishedButton = tk.Checkbutton(
            table,
            variable=self.finished,
            command=self.finishedButton_command,
            width=TODO_ITEM_TABLE_FINISHED_WIDTH,
            justify="center",
        )
        self.finishedButton.grid(row=row_number, column=1)

        self.createdAt = tk.Label(
            table,
            text=str_time(item.created_at),
            width=TODO_ITEM_TABLE_CREATED_AT_WIDTH,
            justify="center",
        )
        self.createdAt.grid(row=row_number, column=2)

        self.remove = tk.Button(
            table,
            text=_("Удалить"),
            command=lambda: self.parent.remove(self.item),
            justify="center",
        )
        self.remove.grid(row=row_number, column=3)

    def finishedButton_command(self):
        self.item.modify(finished=self.finished.get() > 0)


class ToDoListWidget(tk.Frame):
    def __init__(self, *args, delete_list, **argv):
        super().__init__(*args, **argv)
        self.delete_list = delete_list

    def create_table_header(self, body):

        header_font = ("Arial", "10", "bold")
        text = tk.Label(
            body,
            text=_("Текст"),
            width=TODO_ITEM_TABLE_TEXT_WIDTH,
            justify="center",
            font=header_font,
        )
        text.grid(row=0, column=0)

        done = tk.Label(
            body,
            text=_("Выполнено"),
            width=TODO_ITEM_TABLE_FINISHED_WIDTH,
            justify="center",
            font=header_font,
        )
        done.grid(row=0, column=1)

        created = tk.Label(
            body,
            text=_("Создано"),
            width=TODO_ITEM_TABLE_CREATED_AT_WIDTH,
            justify="center",
            font=header_font,
        )
        created.grid(row=0, column=2)

    def create_table(self, itemList):
        table = tk.LabelFrame(self, relief=tk.GROOVE)
        table.grid()
        self.create_table_header(table)

        self.itemList = itemList
        row_number = 1
        for item in itemList:
            item = ToDoItemWidget(self, row_number=row_number, item=item, table=table)
            row_number += 1
        return table

    def create_new_item(self):
        table = tk.LabelFrame(self, relief=tk.GROOVE)
        table.grid()
        self.itemToAdd = tk.Text(table, width=15, height=1)
        self.itemToAdd.grid(row=0, column=0)

        add = tk.Button(table, text=_("Добавить заметку"), command=self.add_command)
        add.grid(row=0, column=1)
        return table

    def fill(self, itemList):
        self.frame = tk.LabelFrame(self, relief=tk.GROOVE)
        self.frame.grid(sticky="NEWS")
        table = self.create_table(itemList)
        table.grid(row=0, column=0)

        new = self.create_new_item()
        new.grid(row=2, column=0)

        delete = tk.Button(self, text=_("Удалить лист"), command=self.delete_list)
        delete.grid(row=4, column=0)

    def update(self, itemList=None):
        self.clear()
        if itemList is None:
            self.fill(self.itemList)
        else:
            self.fill(itemList)

    def add_command(self):
        self.itemList.append(self.itemToAdd.get(1.0, "end"))
        self.update()

    def remove(self, item):
        self.itemList.remove(self.itemList.index(item))
        self.update()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()


class WorkSpaceFrame(tk.Frame):
    def delete_list(self, *args):
        selection = self.listBox.curselection()
        cur = selection[0]
        self.user.removeUserList(self.lists[cur].id)
        self.lists = self.user.fetchUserLists()
        self.update_lists()
        if len(self.lists) > 1:
            self.listBox.selection_set(first=cur - 1)
        elif len(self.lists) > 0:
            self.listBox.selection_set(first=0)

    def __init__(self, user, master=None, url=None) -> None:
        """
        Функция инициаизации класса
        """
        super().__init__(master)

        self.master = master
        self.user = user

        self.pack(fill=tk.BOTH, expand=1)
        self.initLayout(user)

    def destroy(self):
        tk.Tk.destroy(self)
        if self.rbtn_var.get() > 0:
            self.user.save()
        else:
            self.user.remove()

    def initLayout(self, user):

        # Запомнить пользователя
        self.rbtn_var = tk.IntVar(value=1)
        rbtn = tk.Checkbutton(self, text=_("Запомнить меня"), variable=self.rbtn_var, command=None)
        rbtn.pack(anchor="n")

        # data
        self.lists = user.fetchUserLists()

        self.add_list_text = tk.Text(self, width=15, height=1)
        self.add_list_text.pack(anchor="sw")

        add = tk.Button(self, text=_("Добавить лист"), command=self.add_list)
        add.pack(anchor="sw")

        # select list box
        self.listBox = tk.Listbox(self, width=30, selectmode=tk.SINGLE)
        self.listBox.pack(side="left", fill="y")
        self.listBox.bind("<<ListboxSelect>>", self.listBox_selected)

        # scroll bar
        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.config(command=self.listBox.yview)
        scrollbar.pack(side="left", fill="y")

        # add scroll bar to list box
        self.listBox.config(yscrollcommand=scrollbar.set)

        # init list view
        self.update_lists()

        # canvas for todo lists
        canvas = tk.Canvas(self)
        canvas.pack(side="left", fill="both", expand=1)
        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.config(command=canvas.yview)
        scrollbar.pack(side="left", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # todo lists
        self.toDoList = ToDoListWidget(self, delete_list=self.delete_list)
        self.toDoList.grid_propagate(True)
        # self.toDoList = ToDoListWidget(canvas)
        self.toDoList.pack(side="left", fill="y")
        canvas.bind("<Configure>", lambda *argv: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.toDoList, anchor="nw")

        # select list!
        if len(self.lists) > 0:
            self.listBox.selection_set(first=0)
            self.listBox_selected()

    def update_lists(self):
        self.listBox.delete(0, "end")
        for item in self.lists:
            s = f"{str(item)}: {item.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            self.listBox.insert(tk.END, s)
        self.listBox.pack()
        return len(self.lists)

    def add_list(self, *args):
        text = self.add_list_text.get(1.0, "end").strip()
        if len(text) == 0:
            print("empty name! Not adding!")
            return
        self.user.appendUserList(title=text)
        self.lists = self.user.fetchUserLists()

        # fill list box
        self.update_lists()
        len(self.lists) > 0 and self.listBox.selection_set(first=len(self.lists) - 1)

    def listBox_selected(self, *args):
        self.toDoList.clear()

        selection = self.listBox.curselection()
        cur = selection[0]

        self.toDoList.fill(self.lists[cur])
