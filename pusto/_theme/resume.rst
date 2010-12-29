{% extends "base.html" %}
{% block title %}Резюме Костюк Гриши{% endblock %}

{% block content %}
<img src="{{ app.url_for(':theme', path='_images/ava200.jpg') }}" style="float: right" />
{% filter rst %}
Гриша Костюк aka `naspeh </post/unikalniy-nick/>`_
==================================================
* email и jabber: **naspeh(at)gmail.com**
* тел: +380 63 6931716
* г. Днепродзержинск (Украина)
* дата рождения: **15 апреля 1983**


**Цель:** творческая работа в сфере веб-разработки.

**Образование:** законченное высшее. 2000 - 2005 Днепропетровский Национальный Университет, механико-математический факультет. Специалист. Квалификация: механик-исследователь-программист.

**Английский:** средний уровень.


Опыт работы
===========
с 12.2009 веб-разработчик на python в `42 Coffee Cups <http://42coffeecups.com/>`_;
  | 02.2009 - 09.2009 веб-разработчик на Java в `Ardas Group <http://www.ardas.dp.ua/ru>`_;
  | 03.2007 - 02.2009 веб-разработчик на PHP, Freelance;
  | 11.2006 - 03.2007 веб-разработчик на PHP в ЧП «Зебра»;
  | 04.2006 - 10.2006 аналитик в ЧП «Компьютерные технологии и системы»;
  | 02.2005 - 04.2006 оператор 1С в ТК «Сальве».


Собственные проекты
===================
|horosh|_ - проект для публикации отчетов о путешествиях. Стартовал 25.11.2009.
 На нем опробован новый для меня [python][python] фреймворк Pylons_. В качестве JavaScript фреймворка был использован jQuery_. Приложение проектировал удобным, использовал AJAX, но старался не перегибать с последним. Оценить интерфейс редактирования можно по `демо событию <http://horosh.org/demo/>`_. Код доступен на `bitbucket.org <http://bitbucket.org/naspeh/horosh/src>`_.


|naya|_ - микрофреймворк на базе Werkzeug_, используется на этом сайте.
 Werkzeug_ это библиотека(инструмент) для разработки WSGI приложений, но это не фреймворк, поэтому на базе него уже построено не один фреймворк: `Flask <http://flask.pocoo.org>`_, `Tipfy <http://www.tipfy.org/>`_, `Svarga <http://bitbucket.org/piranha/svarga/>`_, `Glashamer <http://glashammer.org/>`_. |naya|_ это еще один :).


Активно использую
=================
* python_ с августа 2009 г; работал с `Django <http://www.djangoproject.com/>`_, Pylons_;  интересуюсь Werkzeug_;
* AJAX/JavaScript работал с jQuery_, `Prototype <http://www.prototypejs.org/>`_;
* (X)HTML/CSS; интересуюсь `семантической версткой <http://pepelsbey.net/2008/04/semantic-coding-1/>`_;
* SQL (MySQL, SQLite);
* `NoSQL <http://ru.wikipedia.org/wiki/NoSQL>`_; интересуюсь `MongoDB <http://www.mongodb.org/>`_;
* `распределённые системы контроля версий (DVCS) <http://habrahabr.ru/blogs/development_tools/71115/>`_: `git <http://git-scm.com/>`_, `mercurial <http://mercurial.selenic.com/>`_;
* пользователь GNU/Linux с июля 2008.

Интересуюсь архитектурой приложений, `паттернами проектирования <http://ru.wikipedia.org/wiki/Шаблон_проектирования>`_, `гибкими методиками разработки <http://ru.wikipedia.org/wiki/Гибкая_методология_разработки>`_, `рефакторингом <http://ru.wikipedia.org/wiki/Рефакторинг>`_, `TDD <http://ru.wikipedia.org/wiki/Разработка_через_тестирование>`_, `свободным ПО <http://ru.wikipedia.org/wiki/Свободное_программное_обеспечение>`_, пользовательскими интерфейсами, `юзабилити <http://ru.wikipedia.org/wiki/Юзабилити>`_. Слежу за новшествами в сфере веб-разработки.

Ранее использовал
=================
* Java с февраля 2009 г (последний раз - сентябрь 2009 г);
* PHP с ноября 2006 г; работал с `Zend Framework <http://framework.zend.com/) (последний раз - март 2009 г>`_.

Личные качества
===============
Стремление к знаниям и идеалам, увлеченный и общительный в общем кругу интересов, честный, спокойный.

Другие интересы и увлечения
===========================
Творчество, созидание, развитие. Семья. Путешествия, велосипед. Играю на бильярде, в футбол, в настольный теннис.

Прочее
======
Не курю, не пью, `женат <http://horosh.org/event-63-karpatyi-chernogorskij-hrebet>`_.

.. |horosh| replace:: **horosh.org**
.. |naya| replace:: **naya**
.. _python: http://python.org/
.. _horosh: http://horosh.org/
.. _naya: http://github.com/naspeh/naya/
.. _jQuery: http://jquery.com/
.. _Werkzeug: http://werkzeug.pocoo.org/
.. _Pylons: http://pylonshq.com/

{% endfilter %}
{% endblock %}
