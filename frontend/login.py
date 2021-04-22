import tkinter as tk
from user import User
import message


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
