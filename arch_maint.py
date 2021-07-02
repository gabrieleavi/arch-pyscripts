# Arch Linux maintenance script written in Python!
# Author : Gabriele Avi
# Version : 0.0.1
# Script creation date: 31 May 2021
# Script begins here

# Importing libraries

import os
import time


# Defining new functions, that will be used in this script and also in others, it is completely customizable
def arch_maint_basic():
    print("Welcome to Arch Linux maintenance script, written entirely in Python!")
    prompt = input("Do you want to continue? [y/N]")
    if prompt == "Y" or prompt == "y":
        print("The script is starting in ")
        for i in range(3, 0, -1):
            print(i, end="... \n")
            time.sleep(1)
        print("now!")
        os.system("paru --noconfirm -Syyu")
    else:
        print("Aborting! Closing the script...", end="\n")
        time.sleep(2)
        exit(0)
    print("The basic script is over! If you want to customize the script, then it will execute after this!")
    time.sleep(5)
    return print("Thank you for using this script!")


# Now here the customization begins if you want to import the basic function you can do it!
if __name__ == '__main__':
    arch_maint_basic()
    # Cleaning the package manager cache, deleting the uninstalled programs' file
    os.system("sudo paccache -ruk0")
    # Cleaning the other cache with paru AUR helper
    os.system("paru -Sc")
    # Using programs to clean the system (e.g. stacer and bleachbit)
    sys_cln = input("Do you use any system cleaning app (e.g. stacer, bleachbit, ...)? [y/n] \n")
    if sys_cln == "y" or sys_cln == "Y":
        os.system("sudo stacer")
        os.system("sudo bleachbit")
    else:
        install = input("Do you want to install any of them? [y/n]\n")
        if install == "Y" or install == "y":
            clean = eval(input("""Which one?
            1.bleachbit
            2.stacer
            : """))
            if clean == 1:
                os.system("sudo pacman --noconfirm -S bleachbit")
                os.system("bleachbit")
            elif clean == 2:
                os.system("paru -S stacer")
                os.system("stacer")

    print("Continuing the script...")
    time.sleep(3)
    reboot = input("Do you wish to reboot? [Y/n] \n")
    if reboot == "Y" or reboot == "y":
        os.system("reboot")
    else:
        print("The customized script ends here! Thank you for your patience!")
        exit(0)
