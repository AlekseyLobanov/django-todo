import gettext
import tkinter as tk

gettext.install("todo", localedir="po")


def str_time(time):
    return time.strftime("%Y-%m-%d %H:%M:%S")


TODO_ITEM_TABLE_TEXT_WIDTH = 15
TODO_ITEM_TABLE_FINISHED_WIDTH = 8
TODO_ITEM_TABLE_CREATED_AT_WIDTH = 15


def placeholder():
    print(_("Не реализовано"))


class ToDoItemWidget(tk.Frame):
    @staticmethod
    def header(parent):
        body = tk.Frame(parent)

        text = tk.Label(body, text=_("Текст"), width=TODO_ITEM_TABLE_TEXT_WIDTH)
        text.pack(side="left")

        text = tk.Label(body, text=_("Выполнено"), width=TODO_ITEM_TABLE_FINISHED_WIDTH)
        text.pack(side="left")

        text = tk.Label(body, text=_("Создано"), width=TODO_ITEM_TABLE_CREATED_AT_WIDTH)
        text.pack(side="left")

        return body

    def __init__(self, *args, item, **argv):
        super().__init__(*args, **argv)

        self.parent = self.master
        self.item = item

        self.noteLabel = tk.Label(self, text=item.text, width=TODO_ITEM_TABLE_TEXT_WIDTH)
        self.noteLabel.pack(side="left")

        self.finished = tk.IntVar(value=int(item.finished))
        self.finishedButton = tk.Checkbutton(
            self,
            variable=self.finished,
            command=self.finishedButton_command,
            width=TODO_ITEM_TABLE_FINISHED_WIDTH,
        )
        self.finishedButton.pack(side="left")

        self.createdAt = tk.Label(
            self, text=str_time(item.created_at), width=TODO_ITEM_TABLE_CREATED_AT_WIDTH
        )
        self.createdAt.pack(side="left")

        self.remove = tk.Button(
            self, text=_("Удалить"), command=lambda: self.parent.remove(self.item)
        )
        self.remove.pack(side="left")

    def finishedButton_command(self):
        self.item.modify(finished=self.finished.get() > 0)


class ToDoListWidget(tk.Frame):
    def __init__(self, *args, delete_list, **argv):
        super().__init__(*args, **argv)
        self.delete_list = delete_list

    def fill(self, itemList):

        header = ToDoItemWidget.header(self)
        header.pack(side="left")
        header.pack(side="top", fill="y")

        self.itemList = itemList

        for item in itemList:
            item = ToDoItemWidget(self, item=item)
            item.pack(side="top", fill="y")

        self.itemToAdd = tk.Text(self, width=15, height=1)
        self.itemToAdd.pack(side="top")

        add = tk.Button(self, text=_("Добавить заметку"), command=self.add_command)
        add.pack(side="top")

        delete = tk.Button(self, text=_("Удалить лист"), command=self.delete_list)
        delete.pack(side="top")

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
