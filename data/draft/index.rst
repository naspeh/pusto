Идеи и черновики
----------------
- napokaz.js, забудьте об бекенде и думайте только об интерфейсе.
- backup скрипт, lvm.
- tider, немного об учете времени.
- wheel, быстрый ``pip install -r requiremnts.txt``.
- меньше кода!
- evilvte крутой терминал.
- archlinux двухлетний полет.
- i3wm управляем окнами клавиатурой.

Live:
  - Москва, гипер-город.


New **pkglist**::

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
