import install
import os
import time
from efi_mbr import *
from ker_and_ed import *


def arch_chroot_install():
        # Keyboard setup
        kb = input("Which keyboard do you use? Please insert it, according to Arch Linux's Official Wiki (e.g. en_us): ")
        os.system("loadkeys {}" .format(kb))
        ker = input("""Please choose the kernel you installed before:
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

        texed = input("""Please select the text editor you installed before:
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
        name = input("Insert the username for your account: ")
        host = input("Please put your desired hostname: ")
        network1, network2, network3 = "127.0.0.1   localhost", "::1    localhost", str("127.0.1.1  {}.localdomain  {}" .format(host, host))
        tz = input("Please insert your time zone from the Arch Wiki (e.g. Europe/Rome): ")
        loc = input("Please input your locale, checking in the Wiki if you don't know it (e.g. en_US.UTF-8): ")
        # Setting the local time and sincronizing the hardware clock to the system clock
        print("Now the script will configure the local time...")
        os.system("ln -sf /usr/share/zoneinfo/{} /etc/localtime" .format(tz))
        os.system("hwclock --systohc")
        print("Now you will be redirected to the /etc/locale.gen file, select the system locale!")
        time.sleep(5)
        # Setting up the locales
        os.system("{} /etc/locale.gen" .format(texed))
        print("Generating the locales...")
        os.system("locale-gen")
        os.system("echo LANG={} /etc/locale.conf" .format(loc))
        os.system("echo KEYMAP={} /etc/vconsole.conf" .format(kb))
        # Setting the hostname and the network file
        os.system("echo {} /etc/hostname" .format(host))
        os.system("echo {} /etc/hosts" .format(network1))
        os.system("echo {} /etc/hosts" .format(network2))
        os.system("echo {} /etc/hosts" .format(network3))
        # Setting the root password
        rootpsw = input("Now you can input the root password... do you want to do it? [y/n] ")
        if rootpsw == "y" or rootpsw == "Y":
            os.system("passwd")
        # Installing the other part of the system
        print("Now the script will install the rest of the system, with the bootloader, etc...")
        time.sleep(2)
        os.system("pacman --noconfirm -S grub os-prober networkmanager network-manager-applet dialog mtools dosfstools ntfs-3g base-devel {}-headers bluez bluez-utils alsa-utils pulseaudio pulseaudio-bluetooth cups git reflector xdg-utils xdg-user-dirs" .format(ker))
        if efi_check():
            os.system("pacman --noconfirm -S efibootmgr")
        # Installing the bootloader
        print("Now the script will install the GRUB bootloader...")
        time.sleep(3)
        os.system("grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB")
        os.system("grub-mkconfig -o /boot/grub/grub.cfg")
        # Activating the services
        print("Now the different services will be activated using systemctl")
        time.sleep(2)
        os.system("systemctl enable NetworkManager")
        os.system("systemctl enable bluetooth")
        os.system("systemctl enable cups")
        # Setting up the user
        os.system("useradd -mG wheel {}" .format(name))
        print("Now you will be redirected to the sudoers file, if you want to give the new account sudo privileges, you can do it now...")
        time.sleep(3)
        os.system("EDITOR={} visudo" .format(texed))
        print("Now the installation is complete, you will need to reboot, after you exited the chroot and umounted all the partition with 'umount -a' ")
        time.sleep(2)
        print("Thank you for using this script!")
