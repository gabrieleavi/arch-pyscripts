"""Defines some basic functions to decide which programs the user choose"""


def ker_decision():
    if ker == "1":
        linux()
    elif ker == "2":
        linux_lts()
    elif ker == "3":
        linux_hardened()
    elif ker == "4":
        linux_zen()


def texed_decision():
    if texed == "1":
        nano()
    elif texed == "2":
        vim()
    elif texed == "3":
        neovim()
    elif texed == "4":
        vi()
