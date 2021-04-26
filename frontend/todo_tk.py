#!/usr/bin/env python3

import sys
import tkinter as tk
from login import LoginFrame
from workspace import WorkSpaceFrame

if "win" in sys.platform.lower():
    DEFAULT_URL = "http://localhost:8000"
else:
    DEFAULT_URL = "http://0.0.0.0:8000"

BASE_W = 580
BASE_H = 400

TITLE_APP = "ToDo Application"


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.center_window()
        self.title(TITLE_APP)

    def login(self):
        """Возвращает пользователя - его можно потом сериализовать"""
        self.frame = LoginFrame(master=self, url=DEFAULT_URL)
        while not self.frame.loggedIn:
            self.update_idletasks()
            self.update()
        self.frame.destroy()
        return self.frame.user

    def main(self, user):
        self.frame = WorkSpaceFrame(master=self, user=user)
        self.mainloop()

    def center_window(self, width: str = BASE_W, heigh: str = BASE_H) -> None:
        """
        Центрирует приложение по центру экрана

        :param width: ширина окна
        :param heigh: высота окна
        """
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        x = (sw - width) / 2
        y = (sh - heigh) / 2
        self.geometry("%dx%d+%d+%d" % (width, heigh, x, y))


if __name__ == "__main__":
    app = Application()
    app.main(app.login())
