.. include:: <s5defs.txt>

.. http://www.youtube.com/watch?v=n4nfjM1ecgw Видео доклада - первый блин комом %)

..
    META{
        "published": "24.02.2013"
    }

==================
Оптимизация тестов
==================

.. class:: center, big

    **на примере Django и PostgreSQL**

.. class:: small

    :Автор: Гриша aka naspeh
    :Команда: `ostrovok.ru <http://ostrovok.ru>`_


.. footer:: ru.pycon 2013

.. contents::
   :class: handout

.. class:: handout

    Люблю три вещи: python, тесты и postgresql, про них и поговорим

    Links:
     - http://blog.endpoint.com/2012/06/speeding-up-integration-tests-with.html
     - http://www.jodal.no/2011/10/19/speeding-up-a-django-web-site-without-touching-the-code/

    rst2s5:
     - http://docutils.sourceforge.net/docs/user/slide-shows.html
     - http://docutils.sourceforge.net/docs/user/slide-shows.txt

.. class:: handout

::

    Какими должны быть тесты?


Если тесты медленные...
-----------------------

* разработчики будут реже запускать
* будут меньше хотеть писать
* медленными будут сборки для CI [*]_

  .. [*] Continuous integration

.. container:: handout

    Для непрерывной  интеграции у нас используется `TeamCity от JetBrains`__

    __ http://www.jetbrains.com/teamcity/

    Оптимизация тестов - важная задача для практик TDD и Continuous integration.


Нужны быстрые тесты
-------------------

* запуск всех - максимально быстрый
* запуск отдельных - очень быстрый
* ... и нужен удобный запуск

.. class:: handout

    * запуск всех - важен в конце фичи и на CI
    * запуск отдельных - ежедневная операция


Задача
------

* ~1000 тестов
* мы не можем использовать SQLite в памяти
* много тестов `поверх WSGI`__
* ~350 тестов с ``commit_on_success``

.. class:: incremental

* нам нужны максимально быстрые тесты...

__ https://docs.djangoproject.com/en/dev/topics/testing/overview/#making-requests

.. class:: handout

::

    ``stat.start_transaction``: 592
    ``stat.start_unique_db``  : 353

    У нас используются специфические возможности PostgreSQL: типы, расширения.

    Треть использует ручное управление транзакциями (в частности ``commit_on_success``),
    почти все эти тесты связаны с бронированием.


Давайте немного позамеряем
--------------------------

| Мерить мы будем стандартное
| поведение django в тестах

| База нашего реального приложения
| с кучей таблиц: **217** штук %)


Параметры системы
-----------------
::

    Железо: Intel Core i5-3210M, SSD, Mem~4GB
    Linux: Kernel~3.7.6-1-ARCH


    PostgreSQL 9.2.3; fsync=off
    Python 2.7.3
    Django 1.4.2

.. class:: handout

    **fsync**::

    > Смысл параметра: Данный параметр отвечает за сброс данных
    > из кэша на диск при завершении транзакций. Если
    > установить его значение fsync = off то данные не будут
    > записываться на дисковые накопители сразу после завершения
    > операций. Это может существенно повысить скорость
    > операций insert и update, но есть риск повредить базу,
    > если произойдет сбой (неожиданное отключение питания,
    > сбой ОС, сбой дисковой подсистемы).


Используемый TestCase
---------------------

.. class:: f65

.. code:: python

    class TestV1(TestCase):
        def test_v0(self):
            res = self.client.get('/admin/orders/order/')
            self.assertContains(res, 'this_is_the_login_form')

        def test_v1(self):
            self.go_to_admin()

        def test_v2(self):
            self.go_to_admin()
            self.go_to_admin('admin2')

        def go_to_admin(self, name='admin', password='password'):
            User.objects.create_superuser(name, None, password)
            self.client.login(username=name, password=password)
            res = self.client.get('/admin/orders/order/')
            self.assertNotContains(res, 'this_is_the_login_form')

.. class:: handout

::

    - v0: мы вообще ничего не меняем в базе (есть несколько select-ов)
    - v1:
      - мы создаем пользователя
      - логируем
      - заходим на страницу в админке
    - в остальных тестах чем больше номер, тем больше повторений шагов из v1

Тесты в транзакции
------------------

.. class:: small

- перед тестом открываем транзакцию: ``begin``
- после - откатываем: ``rollback``

.. class:: tiny

::

    ./manage.py test tt/tests/test_v1.py
    1.34s call     tt/tests/test_v1.py::TestV2::test_v4
    1.29s call     tt/tests/test_v1.py::TestV1::test_v4
    0.96s call     tt/tests/test_v1.py::TestV1::test_v3
    0.96s call     tt/tests/test_v1.py::TestV2::test_v3
    0.89s call     tt/tests/test_v1.py::TestV1::test_v0
    0.66s call     tt/tests/test_v1.py::TestV1::test_v2
    0.66s call     tt/tests/test_v1.py::TestV2::test_v2
    0.35s call     tt/tests/test_v1.py::TestV1::test_v1
    0.34s call     tt/tests/test_v1.py::TestV2::test_v1
    0.04s call     tt/tests/test_v1.py::TestV2::test_v0
    ============ 10 passed in 7.74 seconds =============
    7.82s user 0.36s system 86% cpu 9.492 total

.. class:: green

    Итого: 9.5 секунд, минимум: ~моментально

.. container:: handout

    Все хорошо, если бы нам не нужен был ``commit_on_success``,
    т.е. ручное управление транзакциями

    На выполнение теста тоже нужно время.
    Чем больше операций в тесте - тем он дольше.


Тесты с commit_on_success
-------------------------

.. class:: small

Django подход: очистка базы (flush) перед каждым тестом

.. class:: tiny

::

    $ ./manage.py test tt/tests/test_v1.py
    5.10s call     tt/tests/test_v1.py::TestV2::test_v4
    4.97s call     tt/tests/test_v1.py::TestV1::test_v4
    4.77s call     tt/tests/test_v1.py::TestV2::test_v3
    4.72s call     tt/tests/test_v1.py::TestV1::test_v3
    4.67s call     tt/tests/test_v1.py::TestV1::test_v0
    4.44s call     tt/tests/test_v1.py::TestV2::test_v2
    4.35s call     tt/tests/test_v1.py::TestV1::test_v2
    4.15s call     tt/tests/test_v1.py::TestV1::test_v1
    4.13s call     tt/tests/test_v1.py::TestV2::test_v1
    3.86s call     tt/tests/test_v1.py::TestV2::test_v0
    ============ 10 passed in 45.41 seconds ============
    32.33s user 1.00s system 70% cpu 47.142 total

.. class:: green

    Итого: 47 секунд, минимум: ~4 секунд

.. class:: handout

- ./manage.py flush/sqlflush
- TRUNCATE всех таблиц, и сброс всех sequences
- плюс инициализация базы, но фикстур нет - это быстро


Что это значит?
---------------

* 350 из 1000 тестов с ``commit_on_success``
* итого: 350 * 4 сек = ~23 мин
* и это только чистый ``flush``

.. class:: incremental

* это отстой
* нужен другой механизм обнуления базы...

.. class:: handout

   * 23 мин - это только время на чистый flush, а еще время самих тестов


Уникальная база из шаблона
--------------------------

.. class:: small

- первоначальную базу создаем один раз: ``t_base``
- для каждого теста создаем уникальную базу из ``t_base``

.. code:: sql

    CREATE DATABASE "t_uniq" WITH TEMPLATE "t_base";
    -- запуск теста
    DROP DATABASE "t_uniq";

.. class:: small

**Ограничение:** к шаблону не должно быть подключений

.. class:: handout

Использовать специфичные возможности вашего движка базы дынных - это выход.


Уникальная база, замеряем
-------------------------

.. class:: tiny

::

    ./manage.py test tt/tests/test_v1.py
    1.76s call     tt/tests/test_v1.py::TestV2::test_v4
    1.73s call     tt/tests/test_v1.py::TestV1::test_v4
    1.39s call     tt/tests/test_v1.py::TestV2::test_v3
    1.35s call     tt/tests/test_v1.py::TestV1::test_v3
    1.30s call     tt/tests/test_v1.py::TestV1::test_v0
    1.17s call     tt/tests/test_v1.py::TestV2::test_v2
    1.08s call     tt/tests/test_v1.py::TestV1::test_v2
    0.97s call     tt/tests/test_v1.py::TestV1::test_v1
    0.76s call     tt/tests/test_v1.py::TestV2::test_v1
    0.45s call     tt/tests/test_v1.py::TestV2::test_v0
    ============ 10 passed in 12.20 seconds ============
    7.88s user 0.31s system 58% cpu 13.945 total

.. class:: green

    Итого: 14 секунд, минимум: 0.45 секунды

350 * 0.45 = :red:`2.5 мин` (против :red:`23 мин` для ``flush``)


Сводная таблица
---------------

.. class:: small

========================  ===========  ==============
метод                     всего, сек   минимум, сек
========================  ===========  ==============
в транзакции              9.5          ~0.04
уникальная база           14           ~0.45
очистка базы (``flush``)  47           ~4.00
========================  ===========  ==============

.. class:: incremental

* flush - отстой
* уникальная база - клёво


Полгода назад
-------------

* ~250 тестов
* проходили за 3-4 минуты
* нас это устраивало

.. class:: incremental

* ... но тестов становилось все больше

.. container:: handout

    Полгода назад, во время выхода `статьи на хабре`__ (26 июня 2012),
    у нас было ~250 тестов, проходили они за 3-4 минуты
    и мы радовались - это довольно быстро.

    __ http://habrahabr.ru/company/ostrovok/blog/146552/

    Тогда мы уже использовали уникальную базу вместо flush.

    Время шло, кол-во тестов росло, в приоритете были другие задачи.


3 месяца назад
--------------

* ~800 тестов
* ходили минут 15
* половина времени сборки - наши тесты %)

.. class:: incremental

* ... нужно было тесты параллелить


.. container:: handout

    3 месяца назад тестов было 800 и ходили они минут 15. Долго.

    Сборки пакете на CI сервере были по 30-40 минут.
    Из них почти половина времени - тесты.

    Оптимизации в однопоточном режиме не давали большого прироста.

    Нужно было что-то делать. Нужен был координальный подход.

    Решение очевидное - распараллелить тесты.

    Правда есть пара сдерживающих моментов...
    С таким количеством тестов задача оптимизации тоже усложняется.
    Дольше ходят тесты - дольше разрабатывать тестовую среду.


nose(1.x) и плагины
-------------------

.. class:: handout

    Посмотрим на реализацию того времени.


**Первая реализация тестовой среды:**

* свой раннер на базе ``django_nose``
* свои плагины

.. class:: incremental

* наши плагины не совместимы с multiprocess
* нужно рефакторить...

.. container:: handout

    nose умеет несколько процессов из коробки.
    В django nose multiprocess работает только для SQLite в памяти.

    В последствии оказалось, что множество плагинов не совместимы с multiprocess.

    Даже Xunit отчет, который нужен для CI.

    Если вы только начинаете проект обратите лучше внимание на nose2 и pytest,
    в них совместимость между multiprocess и плагинами - лучше.

    Но nose2 и pytest до конца несовместимы с nose1.


Рефакторинг тестовой среды
--------------------------

* логику с изоляцией базы перенесли в TestCase
* появился пул баз по кол-ву процессов
* для каждого теста блокируем базу

.. class:: handout

::

    Время нашлось нужно было делать рефакторинг.

    1.
      Проверяем, что тест наследуется от нашего TestCase.

      Логика на уровне TestCase нам позволила абстрагироваться от раннера.

      У нас появилась возможность опробовать nose2 и pytest на наших тестах.
      Но пока мы остаемся на nose1.

      pytest в однопоточном режиме работает отлично, а вот
      в несколько потоков выходит дольше чем один, на порядок дольше %)...

    2.
      Пулы создаются на уровне раннера.

      Базы для пула создаются тем же методом что и уникальная база.
      "По шаблону" (``create db ... with template``).

    3.
      Переда запуском блокируем, после - отпускаем.



Запуск тестов в одном процессе
-------------------------------

.. class:: small

::

    $ ./manage.py test
    ---------------------------------------------------
    Ran 945 tests in 1049.055s

    OK (SKIP=14)
    (714.72s user 17.35s system 69% cpu 17:31.64 total)


.. class:: green, big

17-18 минут, это много...


Запуск тестов в несколько процессов
------------------------------------

.. class:: small

::

    $ ./manage.py test --processes=4
    ---------------------------------------------------
    Ran 945 tests in 341.634s

    OK (SKIP=14)
    (917.19s user 15.47s system 267% cpu 5:48.75 total)


.. class:: green

- меньше 6 минут
- быстрее :red:`в 3 раза`
- или быстрее :red:`на 12 минут`

.. class:: incremental, green

    *... то что надо!*

.. container:: handout

    На CI сервере немного дольше, но можно добавить больше processes.

    Для любителей ультрабуков с их низкочастотными процессорами будет дольше.
    Например: для любителей 11-х MacBook Air.
    Но выбор железа остается за разработчиком.
    Производительность рабочего ноутбука - это важно.


.. container:: handout

    Тесты мы ускорили

    1000 тестов за 6 минут:
      * можно подождать
      * или посмотреть на свои изменения еще раз

    Заметки:
     * дальнейшая оптимизация скорее всего будет не такой показательной
     * привязываться к nose1 - сейчас плохая идея


    Дальнейшая оптимизация нужна, т.к. кол-во тестов обычно только растет.
    У нас есть отдельная команда экстранета, которая занимается админкой для отелей.
    В их проекте ~3200 тестов %).


Еще пара приемов
----------------

* свой раннер со своими параметрами
* отдельные настройки для тестов
* изоляция кэшей и redis
* отдельный шаг создания базы


.. class:: handout

   Если хватит времени.

   Расскажу несколько приемов из нашей практики.


Свой раннер
-----------

- подготовка начальной среды (multiprocess)
- различные параметры для удобства (bootstrap)

Так мы переопределили раннер:

.. code:: python
    :class: small

    # testing/management/commands/test.py
    from testing.runner import run

    class Command(object):
        def run_from_argv(self, argv):
            run(argv)


.. class:: handout

    Наш процесс запуска тестов очень изминился,
    нам понадобился свой раннер.

    Добавляем необходимые параметры,
    а также параметры для удобства.

    Мы не используем django параметры - они не нужны.


Отдельные настройки для тестов
------------------------------

- фиксируем специфические настройки
- ... и даже мокаем redis %)


.. class:: small

    При запуске ``./manage.py test`` подхватываются тестовые настройки:

    .. code:: python

        # settings/__init__.py
        if 'test' in sys.argv:
            from .testing import *

.. class:: handout

    Фиксируем разные настройки для тестов


Изоляция кэшей и redis
----------------------
Кэши:
 * используем ``django...LocMemCache``
 * в конце каждого теста - очищаем

Redis:
 * пул для многопроцессорного режима
 * в начале каждого теста блокируем
 * в конце - зачищаем и разблокируем


Отдельный шаг создания базы
---------------------------

**Для быстрого запуска отдельных тестов**

.. class:: green, small

    С созданием базы: 1 тест за ~1 секунду, а ждем ~15 секунд

.. class:: tiny

::

    $ time ./manage.py test tt/tests/test_v1.py:TestV1.test_v0 --create-db
    ----------------------------------------------------------------------
    Ran 1 test in 0.719s
    OK (14.616 total)

.. class:: green, small

    Без создания базы: 1 тест за ~1 секунду, a ждем всего ~3 секунд

.. class:: tiny

::

    $ time ./manage.py test tt/tests/test_v1.py:TestV1.test_v0
    ----------------------------------------------------------------------
    Ran 1 test in 0.810s
    OK (2.641 total)


.. container:: handout

    У нас есть один тест, который мы только что починили
    и хотим проверить, что он проходит.

    Кажется это мелочь 15 секунд, но отзывчивость тестов
    очень важно для частых операций.
    При обычном харде (HDD), это время может быть больше.

    Есть неблольшой минус, что база может изменится,
    и нужно пересаздать базу, но плюсов больше.


Подытожим
---------

* тесты мы ускорили
* сделали удобнее ежедневное использование

.. class:: incremental

* т.е. уменьшили преграды для их написания
* больше хороших тестов даст больше уверенности в коде


Спасибо за внимание
-------------------

.. class:: huge

    Вопросы?


:текст читал: Гриша Костюк
:email: naspeh@gmail.com
:хомяк: `pusto.org <http://pusto.org>`_
:github: `github.com/naspeh <https://github.com/naspeh/>`_

