Tider -- lightweight time tracker (GTK+)
========================================
**Tider** gives answers to several questions:
 - which activity am I working on at the moment?
 - how long have I been working at the moment?
 - is it time to take a break? (informs via notification)
 - which activities have I been working on today?
 - how long have I been working today?
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

    $ pip install https://github.com/naspeh/tider/archive/master.zip

**Installation on Archlinux**::

    $ yaourt -S tider-git

Command line interface
----------------------
Tider can do almost all actions through the command line: open menu, set activity and etc. 
That gives you the ability to setup your custom hotkeys in desktop specific environment. 
For example in i3wm__ you can use ``"~/.i3/config"``, but in Xfce you can use 
``"Application Shortcuts"`` tab::

    Settings > Keyboard > Application Shortcuts

I use sxhkd__ (simple X hotkey daemon) to declare specific hotkeys for such programs.

__ http://i3wm.org/docs/userguide.html#keybindings
__ https://github.com/baskerville/sxhkd

Configuration
-------------
Default config available through command line::

    $ tider conf

There are some regular settings and some hooks. Hooks are needed for integration with 
desktop environment. Config file is located ``"~/.config/tider/config.py"``.

**i3wm and i3status:**
  Modify ``text_hook``:

  .. code:: py

    def text_hook(ctx):
        ...
        import json

        i3bar = json.dumps({'full_text': text, 'color': color})
        with ctx.open('%s/i3bar.txt' % ctx.conf.conf_dir, mode='w') as f:
            f.write(i3bar)
        return markup

  Then use ``"~/.config/tider/i3bar.txt"`` for i3status

**Xfce4 and xfce4-genmon-plugin:**
    Also modify ``text_hook``:

    .. code:: py

        def text_hook(ctx):
            ...
            stats = re.sub(r'<[^>]+>', '', ctx.stats)
            xfce = '<txt>%s</txt><tool>%s</tool>' % (markup, stats)
            with ctx.open('%s/xfce.txt' % ctx.conf.conf_dir, mode='w') as f:
                f.write(xfce)
            return markup

    Then use ``"~/.config/tider/xfce.txt"`` for `xfce4-genmon-plugin`__.

__ http://goodies.xfce.org/projects/panel-plugins/xfce4-genmon-plugin


Reports in terminal
-------------------
Here is a weekly report for two weeks period::

    $ tider re -i2w -w
    Statistics from 2015-03-09 to 2015-03-15
    |target   |       work|  with rest|
    |---------|-----------|-----------|
    |@surf    | 30h 16m 6s|36h 19m 20s|
    |pusto@dev| 3h 23m 42s|  4h 4m 27s|
    |arch@tune|   2h 0m 4s|  2h 24m 5s|
    |lal@mix  | 1h 56m 48s| 2h 20m 10s|
    |tider@dev|     20m 7s|     24m 9s|
    |@fop     |     6m 32s|     7m 51s|
    |---------|-----------|-----------|
    |total    | 38h 3m 19s|45h 39m 59s|

    Statistics from 2015-03-16 to 2015-03-22
    |target    |       work|  with rest|
    |----------|-----------|-----------|
    |@surf     |22h 14m 30s|26h 41m 24s|
    |pusto@text|  2h 53m 3s| 3h 27m 40s|
    |arch@tune |  1h 51m 0s| 2h 13m 12s|
    |lal@mix   | 1h 48m 19s|  2h 9m 59s|
    |pusto@dev |    34m 50s|    41m 48s|
    |----------|-----------|-----------|
    |total     |29h 21m 42s| 35h 14m 3s|

    Statistics from 2015-03-09 to 2015-03-22
    |target    |       work|  with rest|
    |----------|-----------|-----------|
    |@surf     |52h 30m 36s| 63h 0m 44s|
    |pusto@dev | 3h 58m 32s| 4h 46m 15s|
    |arch@tune |  3h 51m 4s| 4h 37m 17s|
    |lal@mix   |  3h 45m 7s|  4h 30m 9s|
    |pusto@text|  2h 53m 3s| 3h 27m 40s|
    |tider@dev |     20m 7s|     24m 9s|
    |@fop      |     6m 32s|     7m 51s|
    |----------|-----------|-----------|
    |total     | 67h 25m 1s| 80h 54m 2s|

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
