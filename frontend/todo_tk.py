#!/usr/bin/env python3
import sys
import tkinter as tk
from tkinter import messagebox as mb
from user import User

if 'win' in sys.platform.lower():
    DEFAULT_URL = "http://localhost:8000"
else:
    DEFAULT_URL = "http://0.0.0.0:8000"

BASE_W = 580
BASE_H = 400


class Application(tk.Frame):
    def __init__(self,
                 master=None
                 ) -> None:
        """
        Функция инициаизации класса
        """
        super().__init__(master)

        #Иницализируем параметры окна
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)

        self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        tk.Grid.rowconfigure(master, 0, weight=1)
        tk.Grid.columnconfigure(master, 0, weight=1)

        # Иницализируем параметры пользователя
        self.user = User(url=DEFAULT_URL)

        # Настраиваем размеры и включаем иницализацию
        self.centerWindow()
        self.initAUTH()

    def centerWindow(self,
                     width: str = BASE_W,
                     heigh: str = BASE_H
                     ) -> None:
        """
        Центрирует приложение по центру экрана

        :param width: ширина окна
        :param heigh: высота окна
        """
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - width) / 2
        y = (sh - heigh) / 2
        self.master.geometry('%dx%d+%d+%d' % (width, heigh, x, y))

    def login_clicked(self) -> None:
        """
        Функция авторизации
        """
        try:
            self.user.auth(self.login.get(), self.password.get())
        except Exception as ex:
            print(ex)
            self.show_info()

    def show_info(selfб,
                  msg: str = None
                  ) -> None:
        """
        Показывает передаваемое сообщение в messagebox

        :param msg: передаваемое сообщение
        """
        if msg is None:
            msg = "Неправильный логин или пароль"
        mb.showinfo("Информация", msg)

    def initAUTH(self) -> None:
        """
        Создает окно авторизации программы
        """
        #Конфигурируем сетку
        for rows in range(25):
            tk.Grid.rowconfigure(self, rows, weight=1)

        for columns in range(25):
            tk.Grid.columnconfigure(self, columns, weight=1)

        # Подпись и поле ввода для логина
        login_label = tk.Label(self, text="Введите логин")
        login_label.grid(row=9, column=12, columnspan=3, rowspan=1, sticky="nsew")

        self.login = tk.Entry(self)
        self.login.grid(row=10, column=12, columnspan=3, rowspan=1, sticky="nsew")

        # Подпись и поле ввода для пароля
        password_label = tk.Label(self, text="Введите пароль")
        password_label.grid(row=11, column=12, columnspan=3, rowspan=1, sticky="nsew")

        self.password = tk.Entry(self, show="*")
        self.password.grid(row=12, column=12, columnspan=3, rowspan=1, sticky="nsew")

        # Кнопка авториазции
        btn = tk.Button(self, text="Войти", command=self.login_clicked)
        btn.grid(row=14, column=12, columnspan=3, rowspan=1, sticky="nsew")


if __name__ == "__main__":
    master = tk.Tk()
    app = Application(master)
    app.master.title("ToDo")
    app.mainloop()
