kernel repair instructions

```
sudo fdisk -l
sudo mkdir /mnt/myos
sudo mount /dev/nvme0n1p2 /mnt/myos

sudo mount --bind /dev /mnt/myos/dev
sudo mount --bind /sys /mnt/myos/sys
sudo mount --bind /proc /mnt/myos/proc
sudo mount --bind /dev/pts /mnt/myos/dev/pts

sudo chroot /mnt/myos

nano /etc/hosts
hostname #<add hostname here>
exit

sudo chroot /mnt/myos
sudo apt update

apt search linux-image
sudo apt install linux-image-5.15.0-100-generic
sudo apt install linux-headers-5.15.0-100-generic

sudo update-grub

exit

sudo umount /mnt/myos/dev/pts
sudo umount /mnt/myos/dev
sudo umount /mnt/myos/proc
sudo umount /mnt/myos/sys
sudo umount /mnt/myos

sudo reboot

```
