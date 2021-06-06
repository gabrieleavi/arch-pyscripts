"""Checks if a computer is running in EFI mode"""


def efi_check():
    import os

    ver_efi = os.popen("ls /sys/firmware/efi").read()
    return ver_efi != ""


def mbr_check():
    import os

    ver_mbr = os.popen("ls /sys/frimware/efi").read()
    return ver_mbr == ""
