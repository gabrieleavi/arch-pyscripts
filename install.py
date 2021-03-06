# Arch linux install script written in Python
# Author : Gabriele Avi
# Version : 0.0.1
# Creation date : 31 May 2021
# Code begins here

from os import system
from time import sleep
from efi_mbr import *
from arch_chroot import *

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
            ker = "linux"
        elif ker == "2":
            ker = "linux-lts"
        elif ker == "3":
            ker = "linux-hardened"
        elif ker == "4":
            ker = "linux-zen"

        texed = input("""Please choose a text editor:
        1. nano
        2. vim
        3. neovim
        4. vi
        (input the full name or number): """)

        if texed == "1":
            texed = "nano"
        elif texed == "2":
            texed = "vim"
        elif texed == "3":
            texed = "neovim"
        elif texed == "4":
            texed = "vi"

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
            db_check = input("Do you want to make a dual boot system? [y/n] ")
            if db_check == "y" or db_check == "Y":
                system("fdisk -l")
                sleep(1)
                efi_user = input("Please insert the existent EFI partition (e.g. /dev/sda1): ")
                print("""You will now be redirected to cfdisk, a CLI (Command Line Interface) tool that will help you manage your disk partitions!
                Please follow the installation wiki for Arch Linux found at this link: https://wiki.archlinux.org/title/Installation_guide. You will only need
                to create a linux filesystem partition and, if you want, a swap partition.""")
                sleep(10)
                system("cfdisk {}" .format(part))
                system("fdisk -l")
                sleep(5)
                check = input("Please input the linux filesystem partition (e.g. /dev/sda5): ")
                swap = input("Please input the swap partition, if you created one in cfdisk (e.g. /dev/sda6): ")
                system("mkfs.ext4 {}" .format(check))
                if swap != "":
                    system("mkswap {}" .format(swap))
                    system("swapon {}" .format(swap))
                system("mount {} /mnt" .format(check))
                system("mkdir -p /mnt/boot/efi")
                system("mount {} /mnt/boot/efi" .format(efi_user))
            else:
                print("The system is using EFI...")
                print("Creating a EFI partition in the disk...")
                # Using parted to partition the drives
                system("parted {} mklabel gpt".format(part))
                system("parted {} mkpart EFI fat32 1Mib 200MiB".format(part))
                system("parted {} mkpart swap linux-swap 200MiB 4GiB".format(part))
                system("parted {} mkpart home ext4 4GiB 100%".format(part))
                print("Mounting the partitions...")
                # Formatting the file systems
                system("mkfs.fat -F32 {}1".format(part))
                system("mkswap {}2".format(part))
                system("swapon {}2".format(part))
                system("mkfs.ext4 {}3".format(part))
                # Mounting the partitions
                system("mount {}3 /mnt".format(part))
                system("mkdir -p -v /mnt/boot/efi")
                sleep(3)
                system("mount -v {}1 /mnt/boot/efi".format(part))
                sleep(3)
                system("lsblk")
                sleep(5)
        if mbr_check():
            print("The system is using MBR...")
            print("Creating the partitions for a MBR system...")
            # Using parted to partition the drives
            system("parted {} mklabel msdos" .format(part))
            system("parted {} mkpart primary ext4 1Mib 100%" .format(part))
            system("parted {} set 1 boot on" .format(part))
            # Formatting the file systems
            system("mkfs.ext4 {}1" .format(part))
            system("mount {}1 /mnt" .format(part))

        # Installing the base packages
        system("clear")
        print("Now the script will install the base packages with pacstrap")
        sleep(3)
        system("pacstrap /mnt base {0} linux-firmware {1} git python3" .format(ker, texed))

        # Generating the fstab
        system("genfstab -U /mnt >> /mnt/etc/fstab")
        print("Now the script will chroot and continue the installation from there!")

        # Chrooting
        system("arch-chroot /mnt")


if __name__ == '__main__':
    arch_install_iso()
