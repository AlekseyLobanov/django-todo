from tkinter import messagebox as mb

TITLE_INFO_BOX = "Сообщение!"
MESSAGE_INVALID_LOGIN = "Неправильный логин или пароль"
MESSAGE_EMPTY = "Сдесь могло быть ваше сообщение"


def infobox(msg: str = None) -> None:
    """
    Показывает передаваемое сообщение в messagebox

    :param msg: передаваемое сообщение
    """
    if msg is None:
        msg = MESSAGE_EMPTY
    mb.showinfo(TITLE_INFO_BOX, msg)


def invalid_login():
    infobox(MESSAGE_INVALID_LOGIN)
