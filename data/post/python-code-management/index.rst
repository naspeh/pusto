.. _fabric: http://docs.fabfile.org/
.. _argparse: http://docs.python.org/library/argparse.html
.. _werkzeug: http://werkzeug.pocoo.org/
.. _naya.script.sh: https://github.com/naspeh/naya/blob/2011.09.12/naya/script.py#L33-97
.. _opster: http://opster.readthedocs.org/

..
 http://docs.python.org/library/subprocess.html#subprocess.check_output перехват вывода
 https://github.com/neithere/argh вместо opster

Python. Управление кодом из консоли
-----------------------------------

..
    META{
        "published": "14.09.2011",
        "aliases": ["/naspeh/python-code-management/"]
    }

.. _summary:

В разработке с python немалую роль играет консоль. Запуск сервера, запуск тестов, работа с `VCS <http://ru.wikipedia.org/wiki/Система_управления_версиями>`_, развертывание (deployment) и т.д. Есть конечно `IDE <http://ru.wikipedia.org/wiki/Интегрированная_среда_разработки>`_, которые предлагают много "плюшек", достаточно сделать всего лишь пару кликов, но это мы прошли.

Дальше поговорим про организацию наших телодвижений в консоли.

.. _bit-3:

Makefile
========

Когда я работал в `42cc <http://42coffeecups.com>`_, в практике у нас было добавление `Makefile <http://ru.wikipedia.org/wiki/Make>`_ в проект, куда записывались часто используемые команды (в `sphinx <http://sphinx.pocoo.org/>`_  пошли тем же путем: `раз <https://bitbucket.org/birkenfeld/sphinx/src/cf794ec8a096/Makefile>`_, `два <https://bitbucket.org/birkenfeld/sphinx/src/cf794ec8a096/doc/Makefile>`_), в итоге работа с проектом сводилась к:

::

  make clean
  make runserver
  make test
  make deploy

так сказать псевдонимы, а команды на самом деле были примерно такие:

.. code-block:: make

    clean:
        -rm *~*
        -find . -name '*.pyc' -exec rm {} \;

    runserver:
        PYTHONPATH=$(PYTHONPATH) python django-project/manage.py runserver

    test:
        PYTHONPATH=$(PYTHONPATH) nosetests --with-django --django-settings=$(test_settings) $(module)

.. _bit-4:

Есть с `Makefile` пара неприятных моментов:
 - отступы в целях должны быть именно `табами`, а не 4 пробела. А с учетом специфики python и его `рекомендаций <http://www.python.org/dev/peps/pep-0008/>`_ были случаи, когда редактор был настроен на замену табов, и чтоб вставить таб нужно было его копировать, смешно :);
 - в задачу можно передавать параметры только через правку файла или задание переменных окружения, это основной минус.

Но в общем подход по минимизации команд мне нравился. Можно переключится на проект, посмотреть `Makefile` и понять что используется. Набирать команды короче. А еще у `Makefile` зачастую есть поддержка автодополнения, что тоже в повседневной разработке упрощает жизнь.

.. _bit-5:

Fabric
======

Потом я услышал про чудо библиотеку для деплоймента fabric_ и стал ее использовать. Но плодить `fabfile.py`, `Makefile` совсем не хотелось. Решил, что если использовать fabric_ для деплоймента, то почему бы не использовать ее и для частых локальных команд:

.. code-block:: python

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

.. _bit-6:

Работа с консолью опять сводится к коротким командам:

::

  fab clean pep8
  fab run
  fab deploy:True

.. _bit-7:

В fabric_ мы уже можем передавать параметры при вызове задачи и это клево.

При использовании fabric_ у меня появился ряд демотиваторов:
 - `специфика <http://docs.fabfile.org/en/1.2.2/usage/fab.html#per-task-arguments>`_ передачи параметров в задачи через двоеточие, не unix стиль;
 - в зависимостях две либы: paramiko_, pycrypto_;
 - пару раз пытался заюзать функции из fabric_ просто в коде, как обычную библиотеку (может так делать не надо было :), но все сводилось к тому, что нужно юзать `fab` команду или отказаться совсем;
 - для меня было удивлением, что fabric_ (или paramiko_) не подхватывает `~/.ssh/config` (хотя ключи и `known_hosts` подхватывает). Т.е. в хостах нужно явно прописывать пользователя, когда пользователь на сервере не совпадает, чтоб задача отработала без паролей по ключам. Хотя этого пользователя `можно прописать в настройках <http://docs.fabfile.org/en/1.2.2/usage/fab.html#settings-files>`_ или задать через параметры.

В принципе это не критичные моменты, библиотека делает свое дело. Для разработки на винде, возможно, это лучшее решение, т.к. тут свой ssh клиент paramiko_, но я - не на винде :).

.. _paramiko: http://www.lag.net/paramiko/
.. _pycrypto: https://github.com/dlitz/pycrypto

.. _bit-8:

"Чистый" python
===============

Со временем понял, что из fabric_ мне больше всего нужны функции `local` и `run`, а мои методы деплоя простые и не нужна особенность fabric_ для работы с множеством серверов.

Итак, чтоб сделать `local` c перехватом вывода и без, нужно всего-то:

.. code-block:: python

    from subprocess import call, Popen, PIPE, STDOUT

    # With capture
    cmd = Popen('ls -la', shell=True, stdout=PIPE, stderr=STDOUT)
    print(cmd.communicate()[0])

    # Without capture
    call('ls -la', shell=True)

..
    import subprocess

    # With capture
    cmd = subprocess.Popen(
        'ls -la', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    print(cmd.communicate()[0])

    # Without capture
    subprocess.call('ls -la', shell=True)

.. _bit-9:

Теперь можно вспомнить про argparse_ и `его сабкоманды <http://docs.python.org/library/argparse.html#sub-commands>`_ и уже можно создавать свои `manage.py` на чистой стандартной библиотеке.

**А что будем делать с деплоем?**

Все просто :) - использовать стандартный клиент `ssh`.


.. code-block:: python

    from subprocess import call

    commands = '&&'.join(['ls -la', 'uptime'])
    call('ssh pusto.org "%s"' % commands, shell=True)

..
    import subprocess

    commands = '&&'.join(['ls -la', 'uptime'])
    subprocess.call('ssh pusto.org "%s"' % commands, shell=True)

Т.е. мы можем делать развертывание проекта при помощи стандартной библиотеки python и клиента ssh, который у меня точно есть под рукой.

.. _bit-10:

Удобство использования
======================

В принципе уже можно было бы остановиться, но писать сабкоманды для argparse_ не очень прикольно, хочется чтоб команды писались легко. Мне нравится больше подход opster_, чем-то он похож на `werkzeug.script <http://werkzeug.pocoo.org/docs/script/>`_ в плане определения параметров, но в werkzeug_ эта функциональность запрещенная. Ну и opster_ это полноценная библиотека. Пара примеров:

.. code-block:: python

    #!/usr/bin/env python
    from naya.script import sh
    from opster import command, dispatch


    @command()
    def code(target='.'):
        '''Check code style'''
        sh('pep8 --ignore=E202 %s' % target, no_exit=True)
        sh('pyflakes %s' % target, no_exit=True)
        sh('git diff | grep -1 print', no_exit=True)


    @command()
    def run(
        hostname=('h', 'localhost', 'server name'),
        port=('p', 5000, 'server port'),
        no_reloader=('', False, 'don\'t use reloader'),
        no_debugger=('', False, 'don\'t use debugger')
    ):
        '''Start a new development server'''
        from werkzeug.serving import run_simple
        app = make_app()
        run_simple(hostname, port, app, not no_reloader, not no_debugger)


    if __name__ == '__main__':
        dispatch()

.. _bit-11:

В предыдущем примере есть naya.script.sh_ - это объект, который предоставляет удобный интерфейс для вызова консольных команд. Чтоб лучше понять, еще пример:

.. code-block:: python

    from naya.script import sh
    from opster import command

    sh.defaults(host='pusto.org', params={
        'activate': 'source .env/bin/activate && which python',
        'env_path': '.env',
        'sock_path': '/tmp/pusto-uwsgi.sock',
        'project_path': '/var/www/nanaya',
    })


    @command()
    def remote(target):
        '''Call remote command'''
        sh(
            ['cd $project_path', '$activate', target],
            params={'m': './manage.py'},
            remote=True
        )


.. _bit-12:

Команда `remote` выполняет код на сервере. Она полезна, когда нужно сделать какое-то разовое действие, чтоб не открывать новую консоль или, например, запустить деплой:

::

  $ ./manage.py remote "$m deploy"

Можно посмотреть еще примеры команд `тут <https://github.com/naspeh/pusto/blob/2011.09.14/manage.py>`_.

.. _bit-13:

Итого
=====

Минимизация команд - это классный подход. Хочется обратить внимание на возможности стандартной библиотеки python и лишний раз задуматься, а стоит ли добавлять в зависимости *"жирную"* библиотеку (аля fabric_)...

..
  Мне нравится naya.script.sh_. Может это не идеальный интерфейс и над ним нужно еще поработать, но если бы что-то подобное было в opster_, было бы заманчиво, т.к. выносить это отдельной библиотекой совсем не охота.

  Мне нравится python :), он дает возможность писать лаконично и побуждает стремиться к минимализму в коде...

**P.S.** Еще пара ссылок на инструменты касающиеся темы: `doit <http://python-doit.sourceforge.net/>`_, `paver <http://paver.github.com/paver/>`_.
