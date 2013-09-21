.. |nose| replace:: **nose**
.. _nose: http://packages.python.org/nose/
.. _nose_alt: http://somethingaboutorange.com/mrl/projects/nose/

Python. Компактные тесты
------------------------
..
    META{
        "published": "15.01.2011",
        "aliases": ["/naspeh/lakonichnost-testov-v-python/"]
    }

.. _summary:

Код в тестах обычно простой, т.к. выполняет довольно тривиальные операции
проверки, сравнения и т.д. Когда много похожего кода, то логично подумать о
его краткости.

.. note::
   |nose|_ у меня давно вошел в набор обязательных инструментов для
   тестирования, так что в примерах есть его влияние.

Подход 1. Класс-контейнер с тестами в виде методов, аля unittest_
=================================================================

.. _unittest: http://docs.python.org/library/unittest.html

.. code:: python

    from unittest import TestCase

    answer = 42


    class TestAnswer(TestCase):
        def setUp(self):
            print('setup')

        def test(self):
            self.assertEquals(answer, 42)

        def tearDown(self):
            print('teardown')

`Исторически сложилось`__, что ``unittest`` использует `верблюжью нотацию`__
для ``setUp``, ``tearDown``, ``assert*`` (``assertTrue``, ``assertEquals``...)
методов. Но в python есть :PEP:`8`, в котором принято использовать подчеркивание
в названиях функций (методов), и в ``nose.tools`` можно найти аналогичные
функции, но с подчеркиванием (``assert_true``, ``assert_equals``) для
любителей :PEP:`8`.

__ http://ru.wikipedia.org/wiki/JUnit
__ http://ru.wikipedia.org/wiki/CamelCase

Подход 2. Модуль с тестами в виде функций
=========================================

.. code:: python

    from nose.tools import assert_equal, with_setup

    answer = 42


    def setup_func():
        print('setup')


    def teardown_func():
        print('teardown')


    @with_setup(setup_func, teardown_func)
    def test_answer():
        assert_equal(answer, 42)

В последнее время **второй подход** компоновки тестов мне все больше нравится.
Почему?

- и в первом и во втором подходе приходится давать имя модулю, который будет
  содержать наши тесты. Но в первом нужно еще придумывать имя классу-контейнеру,
  а т.к. мне нравятся небольшие модули (в них проще ориентироваться), то в
  большинстве случаев название класса - тавтология::

    test_auth.py:TestAuth.test_login
    test_auth.py.test_login

- в первом подходе вроде лучше выглядят ``SetUp``, ``TearDown`` методы, во
  втором приходится импортировать декоратор ``with_setup``. Но и тут можно
  выделить плюс, обычно название класса подбираю по содержимым тестам

  .. code:: python

    class TestAuth(TestCase):
        def test_login()
            ...
        def test_logout()
            ...

  но когда для ``test_login`` нужен ``setUp`` метод, а для ``test_logout`` нет,
  то тут приходится класс-контейнеры компоновать в зависимости от используемых
  ``SetUp``, ``TearDown`` методов. В общем присутствует неоднозначность и это
  не очень хорошо :)

- в классе-контейнере забирается один отступ, а отступы ценны, когда соблюдаешь
  ограничение в 80 символов;

- в первом подходе класс наследуется от ``unittest.TestCase``, при вызове
  каждого ``assert*`` метода логично обращаться к ``self`` и тут опять у нас
  крадут символы::

    self.assertEqual
    assert_equal...4

Для написания тестов можно использовать doctest__
=================================================

__ http://docs.python.org/library/doctest.html

.. code:: python
    :number-lines:

    answer = 42


    def test_answer():
        '''
        >>> answer
        42
        '''
        assert False

Выглядит кратко, хотя конечно такой формат тестов не всегда подходит...

.. note::
  Если запускать через nose_ (**$ nosetests --with-doctest**), то строка **9**
  не вызывается.

Классная вещь assert
====================

.. code:: python

    answer = 43


    def test_answer():
        assert answer == 42

После запуска, вывод:

.. code:: pytb

    $ nosetest
    ======================================================================
    FAIL: test.test_answer
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
        assert answer == 42
    AssertionError

Очень заманчиво: не нужен дополнительный импорт, лаконично. Но вот при выводе
не известно какое значение содержит переменная ``answer``. Правда тут может
порадовать nose_ и даже двумя вариантами:

.. code:: pytb

    $ nosetests --pdb-failures
    ...
    -> assert answer == 42
    (Pdb) answer
    43

приходится вводить **answer** - лишние телодвижения :).

Следующий вариант еще красивее:

.. code:: pytb

    $ nosetest -d
    ======================================================================
    FAIL: test.test_answer
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
        assert answer == 42
    AssertionError:
    >>  assert 43 == 42

так что, в принципе, тесты можно писать через **assert** без потери
информативности вывода, нужно только использовать правильные "пускальщики".

Более краткие сигнатуры
=======================

.. code:: python

    from nose.tools import eq_

    answer = 43


    def test_answer():
        eq_(answer, 42)

После запуска, вывод:

.. code:: pytb

    FAIL: test.test_answer
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
        eq_(answer, 42)
    AssertionError: 43 != 42

Заменили ``assert_equal`` на более короткий вариант ``eq_``, вывод ошибки будет
полностью аналогичен. Т.е. при выводе увидим, что ``answer`` на самом деле
**43** и пойдем сразу искать ошибку в коде. Один нюанс, что тесты не
заканчиваются проверкой на ``eq_`` и ``ok_``, которые есть в ``nose.tools``,
набор методов нужен более обширный...

Интересное по теме
==================

- pytest_ - это аналог nose_, со своими "плюшками", `он умеет`__ запускать
  большинство тестов написанных для nose_.

  __ http://pytest.org/latest/nose.html

- attest_ - интересный подход (python way) от известной команды Pocoo_.
  Пример из документации:

  .. code:: python

    from attest import Tests
    math = Tests()

    @math.test
    def arithmetics():
        """Ensure that the laws of physics are in check."""
        assert 1 + 1 == 2

    if __name__ == '__main__':
        math.run()

- Oktest_ для лаконичности - идея прикольная. Пример из документации:

  .. code:: python

    from oktest import ok

    ok (x) > 0                 # same as assert_(x > 0)
    ok (s) == 'foo'            # same as assertEqual(s, 'foo')
    ok (s) != 'foo'            # same as assertNotEqual(s, 'foo')


.. _pytest: http://pytest.org/
.. _attest: http://github.com/dag/attest
.. _pocoo: http://www.pocoo.org/
.. _oktest: http://packages.python.org/Oktest/

Итого
=====

В **python** есть множество способов для написания и запуска тестов, в статье
упоминаются не все. Если задаться целью, то можно писать красивые и лаконичные
тесты.
