Tider - lightweight time tracker (GTK+)
=======================================
**Tider** gives answers to several questions:
 - which activity I am working on at the moment?
 - how long I have been working at the moment?
 - is it time to take a break? (informs via notification)
 - which activities I have been working on today?
 - how long I have been working today?
 - monthly, weekly, daily reports.

.. raw:: html

    <div class="napokaz"
        data-box-width="6"
        data-picasa-user="naspeh"
        data-picasa-album="Pusto"
        data-picasa-filter="tider">
    </div>

Installation
------------
Code available on `github <https://github.com/naspeh/tider>`_

Tider requires ``Python>=3.3`` and ``GTK3``, optional ``notify-send`` for notifications.

::

    $ pip install -e git+git@github.com:naspeh/tider.git#egg=tider

**Installation on Archlinux**::

    $ yaourt -S tider-git

Command line interface
----------------------
Almost all actions Tider can do through the command line: open menu, set activity and etc. 
That give you ability to setup your custom hotkeys in desktop specific environment. For 
example in i3wm__ I use ``"~/.i3/config"``, but in Xfce I use ``"Application Shortcuts"`` 
tab::

    Settings > Keyboard > Application Shortcuts

__ http://i3wm.org/docs/userguide.html#keybindings

Reports in terminal
-------------------
There is weekly report for two weeks period::

    $ tider re -i1703-2903 -w
    Statistics from 2014-03-17 to 2014-03-23
    |target  |       work|      break|
    |--------+-----------+-----------|
    |mail@dev| 32h 59m 7s|         0s|
    |@surf   | 14h 4m 50s|         0s|
    |--------+-----------+-----------|
    |total   | 47h 3m 57s|         0s|

    Statistics from 2014-03-24 to 2014-03-29
    |target    |       work|      break|
    |----------+-----------+-----------|
    |@surf     |19h 56m 20s|         0s|
    |pusto@text| 5h 41m 23s|         0s|
    |mail@dev  |   5h 5m 9s|         0s|
    |eng@text  |  4h 15m 4s|         0s|
    |----------+-----------+-----------|
    |total     |34h 57m 56s|         0s|

    Statistics from 2014-03-17 to 2014-03-29
    |target    |       work|      break|
    |----------+-----------+-----------|
    |mail@dev  | 38h 4m 16s|         0s|
    |@surf     | 34h 1m 10s|         0s|
    |pusto@text| 5h 41m 23s|         0s|
    |eng@text  |  4h 15m 4s|         0s|
    |----------+-----------+-----------|
    |total     | 82h 1m 53s|         0s|

Database
--------
Tider uses one simple sqlite table for saving activities named ``log`` and one pretty view
named ``log_pretty``, so it is easy to use SQL for getting specific report or fix 
something that you can't do via GUI.

Run default sqlite manager with related database::

    $ tider db

Query example::

    sqlite> select id, target, work_m, start_str, end_str from log_pretty limit 3;
    id          target      work_m      start_str            end_str
    ----------  ----------  ----------  -------------------  -------------------
    1785        pusto@text  31          2014-03-29 15:04:04  2014-03-29 15:36:02
    1784        pusto@text  56          2014-03-29 12:21:33  2014-03-29 13:17:53
    1783        mail@dev    92          2014-03-29 10:14:00  2014-03-29 11:46:54
