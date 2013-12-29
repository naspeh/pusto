.. _maximus: http://packages.debian.org/sid/maximus
.. _devilspie: http://www.foosel.org/linux/devilspie
.. |gnome| replace:: **gnome**

..
   http://www.burtonini.com/blog/computers/devilspie
   http://live.gnome.org/DevilsPie
   http://help.ubuntu.ru/wiki/devilspie (ru)

Gnome2 и маленький экран
------------------------
..
    META{
        "published": "28.09.2011",
        "aliases": ["/naspeh/gnome-optimizaciya-okon/"]
    }

В статье покажу как оптимизирую рабочий стол для маленького разрешения ноутбука
(1280х800) и рассмотрю пару полезных утилит для работы с окнами в |gnome|
**второй** версии.

- maximus_ убирает декорацию для максимизированного окна
  (по умолчанию максимизирует все окна);
- devilspie_ позволяет сделать определенные дейсвия (focus, maximize и т.д.)
  с окном по его атрибутам.

.. MORE

Так повелось, что |gnome| у меня стал рабочим столом в **linux**. И так
сложилось, что решил использовать ноутбук "по полной", как рабочую лошадку, чтоб
не возится с синхронизацией данных на нескольких рабочих машинах. Поэтому работу
за ноутбуком нужно было сделать максимально удобной.

.. container:: note

    Возможно скоро променяю |gnome| на какой-нибудь `тайловый оконный менеджер`__  и 
    debian_ на archlinux_, поэтому решил записать этот рецепт, которым пользуюсь уже 
    давно, может кому еще пригодится.

__ http://ru.wikipedia.org/wiki/Фреймовый_оконный_менеджер_X_Window_System
.. _debian: http://www.debian.org/
.. _archlinux: http://www.archlinux.org/

До этого любил сидеть за монитором с большим разрешением 1600x1200
(Samsung-SyncMaster-204b, 20 дюймов), и когда садился за ноут (1280х800)
мне было неудобно, что на экране мало всего помещается. **Решение**: нужно по
максимуму оптимизировать визуальное пространство, занимаемое приложениями.

Первым делом думал избавиться от одной из панелей (по умолчанию в |gnome|
их две, внизу и вверху экрана). Верхняя панелька мне очень понравилась еще при
первом запуске |gnome| и ее удалять совсем не хотелось. Но места на ней совсем
не хватало еще и для списка окон:

.. image:: _img/panel-top.png

Список окон мне тоже оказался очень нужен и желательно, чтоб места для него
было побольше:

.. image:: _img/panel-bottom.png

Панельки так и остались у меня на своих местах :) как в **debian** по умолчанию.
Я пробовал для них автоскрытие, но не пошло. Про режим на весь экран у
приложений тоже помнил, но мне нужны были панельки, т.к. постоянно их использую.

Нужно было оптимизировать пространство между этими панельками.

Maximus_
========

**Декорация окон**. Когда окно не развернуто на весь рабочий стол, то в
декорациях есть смысл: потянуть за заголовок, растянуть окно. А вот когда окно
максимизировано, то частично смысл в декорациях теряется, да еще и место
занимают. Действия типа: скрыть окно ``(Alt+F9)``, закрыть окно ``(Alt+F4)``,
максимизировать ``(Alt+F10)`` хорошо выполняются через быстрые клавиши.
Поэтому убираем декорацию окон, когда они максимизированы. Для этого есть
пакет maximus_ в **debian**:

::

  $ aptitude install maximus

.. container:: note

    В openbox_ есть такой пункт в меню окна: убрать декорацию, но у меня пока стандартный 
    metacity_.

.. _openbox: http://ru.wikipedia.org/wiki/Openbox
.. _metacity: http://ru.wikipedia.org/wiki/Metacity

По умолчанию maximus_ разворачивает все окна на весь экран. Есть `вариант`__
прописывать `exclude_class`, но я поступил по-другому - отключил максимизацию::

  $ gconftool -s /apps/maximus/no_maximize --type bool true
  $ gconftool -R /apps/maximus                             
   undecorate = true
   binding = disabled
   exclude_class = [Totem,Gnome-system-monitor]
   no_maximize = true

Т.е. максимизировать окна буду вручную через ``Alt+F10``.

__ http://www.zhart.ru/software/21-gnome-panel-minimize-in-ubuntu-linux

В общем уже неплохо, но ряд приложений после запуска нужно сразу
максимизировать, т.к. они не хотят запоминать своих размеров и положения...
Лишние телодвижения: запустить, нажать ``Alt+F10``, а хочется просто запустить.

Devilspie_
==========

И тут на помощь приходит devilspie_. Он может работать не только с классами окон
(`exclude_class` из maximus_ - это список классов окон), но и может проверить
имя приложения, класс и имя окна `и еще ряд атрибутов`__. Причем может
`проверить атрибут`__ не только на соответствие, а и на содержание (contains) и
соответствие регулярному выражению. `Действия`__ над окнами тоже разные:
maximize, unmaximize, focus и undecorate даже :).

__ http://www.foosel.org/linux/devilspie#matchers
__ http://www.foosel.org/linux/devilspie#string_tests
__ http://www.foosel.org/linux/devilspie#actions

Инструмент нашли, дальше используем.

::

  $ aptitude install devilspie

Создаем файл ``~/.devilspie/common.ds``. И помещаем туда что-то типа:

.. code:: py
    :number-lines:

    (begin
        ;(debug)
        (if
            (or
                (contains(application_name) "Vim")
                (contains(application_name) "Terminal")
                (contains(window_name) "New Tab - Google Chrome")
                (contains(window_name) "FatRat")
                (contains(window_name) "Document Viewer")
                (contains(window_name) "Clementine")
                (is(window_name) "DreamPie")
            )
            (maximize)
        )
    )

И добавляем ``devilspie`` в автозагрузку.

Обычно работаю с конфигом ``~/.devilspie/common.ds`` следующим образом.
Добавляю строку с дебагом (например: убрать ";" в начале строки №2 в приведенном
выше листинге), убиваю процесс ``devilspie`` и запускаю его в терминале.
В терминал начинают писаться атрибуты окон. Пример сессии::

   $ killall devilspie
   $ devilspie

    Window Title: 'naspeh@free: '; Application Name: 'Terminal'; Class: 'Gnome-terminal'; Geometry: 1280x774+0+3
    Window Title: 'pusto.org: Edit for fun - Iceweasel'; Application Name: 'Iceweasel'; Class: 'Iceweasel'; Geometry: 1280x774+0+3
    Window Title: 'x-nautilus-desktop'; Application Name: 'File Manager'; Class: 'Nautilus'; Geometry: 1280x800+0+0
    Window Title: 'Bottom Expanded Edge Panel'; Application Name: 'Bottom Expanded Edge Panel'; Class: 'Gnome-panel'; Geometry: 1280x24+0+776
    Window Title: 'Top Expanded Edge Panel'; Application Name: 'Top Expanded Edge Panel'; Class: 'Gnome-panel'; Geometry: 1280x25+0+0    

Потом открываю нужное мне окно, смотрю атрибуты, правлю конфиг, перезапускаю
``devilspie`` и так пока не будет все хорошо :).

Раз уж используем devilspie_, можно с его помощью еще что-то замутить.

Например, **Skype** очень жутко ведет себя в **linux**. Один из боков: хочется
чтоб окна чатов открывались в одном месте и одинакового размера. Если заниматься
этим вручную, то тут нужно подгонять каждое новое окно чата мышкой, изрядно
потыкав. И тут на помощь приходит действие ``geometry`` из devilspie_.

Пример debug::

  Window Title: 'Skype? 2.2 (Beta) for Linux'; Application Name: 'Skype? 2.2 (Beta) for Linux'; Class: 'Skype'; Geometry: 266x487+0+25
  Window Title: 'Anastasie - Skype? Chat'; Application Name: 'Skype'; Class: 'Skype'; Geometry: 824x619+456+95

.. code:: py

    (if

        (and
            (contains(window_name) "Skype")
            (matches(window_role) "ConversationsWindow")
        )
        (geometry "800x675+365-0")
    )

Для получения ``window_role`` использовал xprop__, который содержится в ``x11-utils``.

.. __: http://www.x.org/archive/X11R7.5/doc/man/man1/xprop.1.html

Итого
=====

Есть действия, которые каждодневно повторяются, и если на них потратить немного
времени и автоматизировать, то в конечном счете сэкономится пара ненужных
телодвижений в день :). Как говорится: настрой свой **linux** под себя.

Напоследок скриншот экрана:

.. image:: _img/screenshot.png
