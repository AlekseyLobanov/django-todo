#!/usr/bin/env python3

import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)


if __name__ == "__main__":
    app = Application()
    app.master.title("ToDo")
    app.mainloop()
