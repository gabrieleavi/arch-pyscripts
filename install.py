# Arch linux install script written in Python
# Author : Gabriele Avi
# Version : 0.0.1
# Creation date : 31 May 2021
# Code begins here

from os import system
from time import sleep
from efi_mbr import *
from ker_and_ed import *
from arch_chroot import arch_chroot_install
from partitions import *

def arch_install_iso():
    print("Welcome to the Arch Linux Install script! It will guide you through all the process to have a complete system working!")
    confirm = input("Do you want to start the script? Write 'yes' if you want to do so: ")
    if confirm == "yes" or confirm == "Yes" or confirm == "YES":
        print("Script will start in ", end="")
        for i in range(3, 0, -1):
            print(i, end="...\n")
            sleep(1)
        print("now!")
        kb = input("Which keyboard do you use? Please insert it, according to Arch Linux's Official Wiki (e.g. en_us): ")
        # Keyboard setup
        # Verify if the system is EFI or not
        system("loadkeys {}" .format(kb))
        # User input of preferred packages
        ker = input("""Please choose the desired kernel:
        1. linux
        2. linux-lts
        3. linux-hardened
        4. linux-zen
        (input the full name or number): """)

        if ker == "1":
            linux()
        elif ker == "2":
            linux_lts()
        elif ker == "3":
            linux_hardened()
        elif ker == "4":
            linux_zen()

        texed = input("""Please choose a text editor:
        1. nano
        2. vim
        3. neovim
        4. vi
        (input the full name or number): """)

        if texed == "1":
            nano()
        elif texed == "2":
            vim()
        elif texed == "3":
            neovim()
        elif texed == "4":
            vi()

        # Verifying network connection
        network = input("Do you have an Internet connection ready? [y/n] ")
        if network == "Y" or network == "y":
            # Sincronising the time with Internet
            system("timedatectl set-ntp true")
            # Updating the mirrors with reflector
            system("reflector --sort rate -p https -l 10 --save /etc/pacman.d/mirrorlist")
            system("pacman -Syy")
        else:
            wcn = input("Do you want to configure wireless network? [y/n] ")
            if wcn == "y" or wcn == "Y":
                print("""You will be redirected to iwctl to configure your wireless network, use 'station NameOfTheStation get-networks' to get existing networks
                and then 'station NameOfTheStation connect NameOfTheNetwork' to connect to the network""")
                sleep(5)
                system("iwctl")

        # Disk partitioning
        print("Now you will need to configure the disk:")
        system("fdisk -l")
        sleep(5)
        part = input("Select the desired disk you want to partition (e.g. /dev/sda) ")
        print("Partitioning the drive...")
        if efi_check():
            efi_partition()
        if mbr_check():
            mbr_partition()

        # Installing the base packages
        system("clear")
        print("Now the script will install the base packages with pacstrap")
        sleep(3)
        system("pacstrap /mnt base {0} linux-firmware {1}" .format(ker, texed))

        # Generating the fstab
        system("genfstab -U /mnt >> /mnt/etc/fstab")
        print("Now the script will chroot and continue the installation from there!")

        # Chrooting
        system("arch-chroot /mnt")


if __name__ == '__main__':
    arch_install_iso()
    arch_chroot_install()
