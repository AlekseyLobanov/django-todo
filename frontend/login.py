import gettext
import os
import tkinter as tk
from .user import User
from . import message

gettext.install("todo", os.path.join(os.path.dirname(__file__), "po"))


class LoginFrame(tk.Frame):

    loggedIn = False

    def __init__(self, master=None, url=None) -> None:
        """
        Функция инициаизации класса
        """
        super().__init__(master)

        # Иницализируем параметры окна
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)

        # self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        # tk.Grid.rowconfigure(master, 0, weight=1)
        # tk.Grid.columnconfigure(master, 0, weight=1)

        # Иницализируем параметры пользователя
        self.user = User(url=url)

        # Настраиваем размеры и включаем иницализацию
        self.initAUTH()

    def login_clicked(self) -> None:
        """
        Функция авторизации
        """
        try:
            self.user.auth(self.login.get(), self.password.get())
            self.loggedIn = True
        except Exception as ex:
            print(ex)
            message.invalid_login()

    # Если захочется реализовать в логине
    """
    @property
    def remember(self):
        return self.rbtn_var.get()
    """

    def initAUTH(self) -> None:
        """
        Создает окно авторизации программы
        """
        # Конфигурируем сетку
        for rows in range(25):
            tk.Grid.rowconfigure(self, rows, weight=1)

        for columns in range(25):
            tk.Grid.columnconfigure(self, columns, weight=1)

        # Подпись и поле ввода для логина
        t = _("Введите логин")
        login_label = tk.Label(self, text=t)
        login_label.grid(row=9, column=12, columnspan=3, rowspan=1, sticky="nsew")

        self.login = tk.Entry(self)
        self.login.grid(row=10, column=12, columnspan=3, rowspan=1, sticky="nsew")

        # Подпись и поле ввода для пароля
        password_label = tk.Label(self, text=_("Введите пароль"))
        password_label.grid(row=11, column=12, columnspan=3, rowspan=1, sticky="nsew")

        self.password = tk.Entry(self, show="*")
        self.password.grid(row=12, column=12, columnspan=3, rowspan=1, sticky="nsew")

        # Кнопка авториазции
        btn = tk.Button(self, text=_("Войти"), command=self.login_clicked)
        btn.grid(row=14, column=12, columnspan=3, rowspan=1, sticky="nsew")

        # Если захочется реализовать в логине
        """
        # Запомнить пользователя
        self.rbtn_var = tk.IntVar(value=0)
        rbtn = tk.Checkbutton(
            self,
            text="Запомнить меня",
            variable=self.rbtn_var,
            command=None
        )
        rbtn.grid(row=15, column=12, columnspan=3, rowspan=1, sticky="nsew")
        """
