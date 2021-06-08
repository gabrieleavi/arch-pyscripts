"""Functions to partition the disk, both UEFI and MBR"""


def efi_partition():
    print("The system is using EFI...")
    print("Creating a EFI partition in the disk...")
    # Using parted to partition the drives
    system("parted {} mklabel gpt" .format(part))
    system("parted {} mkpart fat32 1Mib 200MiB")
    system("parted {} mkpart linux-swap 200MiB 4GiB" .format(part))
    system("parted {} mkpart ext4 4GiB 100%" .format(part))
    print("Mounting the partitions...")
    # Formatting the file systems
    system("mkfs.fat -F32 {}1" .format(part))
    system("mkswap {}2" .format(part))
    system("swapon {}2" .format(part))
    system("mkfs.ext4 {}3" .format(part))
    # Mounting the partitions
    system("mount {}3 /mnt" .format(part))
    system("mkdir -p /mnt/boot/efi")
    system("mount {}1 /mnt/boot/efi")


def mbr_partition():
    print("The system is using MBR...")
    print("Creating the partitions for a MBR system...")
    # Using parted to partition the drives
    system("parted {} mklabel mbr" .format(part))
    system("parted {} mkpart primary ext4 1Mib 100%")
    system("parted set 1 boot on")
    # Formatting the file systems
    system("mkfs.ext4 {}1" .format(part))
    system("mount {}1 /mnt" .format(part))
