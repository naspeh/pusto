Python. Управление кодом из консоли
-----------------------------------

..
    META{
        "published": "14.09.2011",
        "aliases": ["/naspeh/python-code-management/"]
    }

В разработке с python немалую роль играет консоль. Запуск сервера, запуск
тестов, работа с VCS_, развертывание (deployment) и т.д. Есть конечно IDE_,
которые предлагают много "плюшек", достаточно сделать всего лишь пару кликов,
но это мы прошли.

Дальше поговорим про организацию наших телодвижений в консоли.

.. _VCS: http://ru.wikipedia.org/wiki/Система_управления_версиями
.. _IDE: http://ru.wikipedia.org/wiki/Интегрированная_среда_разработки

.. MORE

Makefile_
=========

Когда я работал в 42cc_, в практике у нас было добавление Makefile_ в проект,
куда записывались часто используемые команды, в итоге работа с проектом
сводилась к::

  make clean
  make runserver
  make test
  make deploy

.. _42cc: http://42coffeecups.com

так сказать псевдонимы, а команды на самом деле были примерно такие:

.. code:: make

    clean:
        -rm *~*
        -find . -name '*.pyc' -exec rm {} \;

    runserver:
        PYTHONPATH=$(PYTHONPATH) python django-project/manage.py runserver

    test:
        PYTHONPATH=$(PYTHONPATH) nosetests --with-django --django-settings=$(test_settings) $(module)

.. note:: В sphinx_  пошли тем же путем: `раз`__, `два`__

.. _sphinx: http://sphinx.pocoo.org/
__ https://bitbucket.org/birkenfeld/sphinx/src/cf794ec8a096/Makefile
__ https://bitbucket.org/birkenfeld/sphinx/src/cf794ec8a096/doc/Makefile

Есть с ``Makefile`` пара неприятных моментов:
 - отступы в целях должны быть именно `табами`, а не 4 пробела. А с учетом
   специфики python и его `рекомендаций`__ были случаи, когда редактор был
   настроен на замену табов, и чтоб вставить таб, нужно было его копировать %);
 - в задачу можно передавать параметры только через правку файла или задание
   переменных окружения, это основной минус.

__ http://www.python.org/dev/peps/pep-0008/

Но в общем подход по минимизации команд мне нравился. Можно переключиться на
проект, посмотреть ``Makefile`` и понять что используется. Набирать команды
короче. А еще у ``Makefile`` зачастую есть поддержка автодополнения, что тоже в
повседневной разработке упрощает жизнь.


Fabric_
=======

Потом я услышал про чудо библиотеку для деплоймента fabric_ и стал ее
использовать. Но плодить ``fabfile.py``, ``Makefile`` совсем не хотелось.
Решил, что если использовать ``fabric`` для деплоймента, то почему бы не
использовать ее и для частых локальных команд:

.. code:: python

    from fabric.api import local, run, cd


    def run():
        '''Start development server'''
        local('PYTHONPATH=. paster serve --reload development.ini', capture=False)


    def pep8(target='.'):
        '''Run pep8'''
        local('pep8 --ignore=E202 %s' % target, capture=False)


    @hosts('root@pusto.org')
    def deploy(restart=False):
        '''Deploy to remote server'''
        local('hg push', capture=False)
        with cd('/var/www/horosh/'):
            run('hg pull&&hg up')
            if restart:
                run('/etc/init.d/horosh force-reload')

Работа с консолью опять сводится к коротким командам::

  fab clean pep8
  fab run
  fab deploy:True

В ``fabric`` мы уже можем передавать параметры при вызове задачи и это клево.

При использовании ``fabric`` у меня появился ряд демотиваторов:
 - `специфика`__ передачи параметров в задачи через двоеточие, не unix стиль;
 - в зависимостях две либы: paramiko_, pycrypto_;
 - пару раз пытался заюзать функции из ``fabric`` просто в коде, как обычную
   библиотеку (может так делать не надо было :), но все сводилось к тому,
   что нужно юзать ``fab`` команду или отказаться совсем;
 - для меня было удивительным, что ``fabric`` (или ``paramiko``) не подхватывает
   ``~/.ssh/config`` (хотя ключи и ``known_hosts`` подхватывает). Т.е. в хостах
   нужно явно прописывать пользователя, когда пользователь на сервере не
   совпадает, чтоб задача отработала без паролей по ключам. Хотя этого
   пользователя `можно прописать в настройках`__ или задать через параметры.

__ http://docs.fabfile.org/en/1.2.2/usage/fab.html#per-task-arguments
__ http://docs.fabfile.org/en/1.2.2/usage/fab.html#settings-files

В принципе это не критичные моменты, библиотека делает свое дело. Для разработки
на винде, возможно, это лучшее решение, т.к. тут свой ssh клиент ``paramiko``,
но я - не на винде :).

.. _paramiko: http://www.lag.net/paramiko/
.. _pycrypto: https://github.com/dlitz/pycrypto

"Чистый" python
===============

Со временем понял, что из ``fabric`` мне больше всего нужны функции ``local`` и
``run``, а мои методы деплоя простые и не нужна особенность ``fabric`` для
работы с множеством серверов.

Итак, чтоб сделать ``local`` c перехватом вывода и без, нужно всего-то:

.. code:: python

    from subprocess import call, Popen, PIPE, STDOUT

    # With capture
    cmd = Popen('ls -la', shell=True, stdout=PIPE, stderr=STDOUT)
    print(cmd.communicate()[0])

    # Without capture
    call('ls -la', shell=True)


Теперь можно вспомнить про `argparse и его сабкоманды`__ и уже можно создавать
свои ``manage.py`` на чистой стандартной библиотеке.

__ /post/python-argparse-subcommands/

**А что будем делать с деплоем?**

Все просто :) - использовать стандартный клиент ``ssh``.


.. code:: python

    from subprocess import call

    commands = '&&'.join(['ls -la', 'uptime'])
    call('ssh pusto.org "%s"' % commands, shell=True)

Т.е. мы можем делать развертывание проекта при помощи стандартной библиотеки
python и клиента ssh, который у меня точно есть под рукой.

Итого
=====
Минимизация команд - это классный подход. Хочется обратить внимание на
возможности стандартной библиотеки python и лишний раз задуматься, а стоит ли
добавлять в зависимости проекта *"жирную"* библиотеку (аля ``fabric``)...

**P.S.** Еще пара ссылок на инструменты касающиеся темы: `doit`_, `paver`_.

.. _Makefile: http://ru.wikipedia.org/wiki/Make
.. _fabric: http://docs.fabfile.org/
.. _doit: http://python-doit.sourceforge.net/
.. _paver: http://paver.github.com/paver/
