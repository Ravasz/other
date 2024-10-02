kernel repair instructions

sudo fdisk -l
sudo mkdir /mnt/myos
sudo mount /dev/nvme0n1p2 /mnt/myos

sudo mount --bind /dev /mnt/myos/dev
sudo mount --bind /sys /mnt/myos/sys
sudo mount --bind /proc /mnt/myos/proc
sudo mount --bind /dev/pts /mnt/myos/dev/pts

sudo chroot /mnt/myos

nano /etc/hosts
hostname 
