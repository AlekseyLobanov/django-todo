import gettext
import os
from tkinter import messagebox as mb

gettext.install("todo", os.path.join(os.path.dirname(__file__), "po"))

TITLE_INFO_BOX = _("Сообщение!")
MESSAGE_INVALID_LOGIN = _("Неправильный логин или пароль")
MESSAGE_EMPTY = _("Сдесь могло быть ваше сообщение")


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
