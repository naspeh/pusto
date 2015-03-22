# New pkglist
```bash
mkfs.ext4 /dev/pad/test
mount /dev/pad/test /mnt
pacstrap -c /mnt base base-devel python
rsyncc /home/{pacman,dotfiles} /mnt/home/
arch-chroot /mnt /bin/bash
/home/dotfiles/bin/pkglist -u
pacman --config=/home/pacman/pacman.conf -S $(cat /home/pacman/{main.txt,abs.txt})
mount /dev/pad/arch /mnt
rsync -aAXHvh /mnt/backup/latest/{etc,home,root} /
vim /etc/fstab
```
