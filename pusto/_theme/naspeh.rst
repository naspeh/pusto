{% extends "base.html" %}
{% block title %}Гриша aka naspeh{% endblock %}

{% macro profile() %}
<img src="{{ app.url_for(':theme', path='_images/ava200.jpg') }}" style="float: right" />
{% filter rst %}

Гриша aka `naspeh </post/unikalniy-nick/>`_
===========================================
email и jabber: **naspeh(at)gmail.com**

С декабря 2009 веб-разработчик на python в `42 Coffee Cups <http://42coffeecups.com>`_.

Собственные проекты
===================
|horosh|_ - проект для публикации отчетов о путешествиях, стартовал 25.11.2009, код доступен на `bitbucket <http://bitbucket.org/naspeh/horosh/src>`_.

|naya|_ - микрофреймворк на базе Werkzeug_, используется на этом сайте.


Активно использую
=================
* python_ с августа 2009 г; работал с `Django <http://www.djangoproject.com/>`_, Pylons_;  интересуюсь Werkzeug_;
* AJAX/JavaScript работал с jQuery_, `Prototype <http://www.prototypejs.org/>`_;
* (X)HTML/CSS; интересуюсь `семантической версткой <http://pepelsbey.net/2008/04/semantic-coding-1/>`_;
* SQL (MySQL, SQLite);
* `NoSQL <http://ru.wikipedia.org/wiki/NoSQL>`_; интересуюсь `MongoDB <http://www.mongodb.org/>`_;
* `распределённые системы контроля версий (DVCS) <http://habrahabr.ru/blogs/development_tools/71115/>`_: `git <http://git-scm.com/>`_, `mercurial <http://mercurial.selenic.com/>`_;
* пользователь GNU/Linux с июля 2008; `Debian GNU/Linux <http://www.debian.org/>`_ и `Vim <http://www.vim.org/>`_ с августа 2010.

Интересуюсь архитектурой приложений, `паттернами проектирования <http://ru.wikipedia.org/wiki/Шаблон_проектирования>`_, `гибкими методиками разработки <http://ru.wikipedia.org/wiki/Гибкая_методология_разработки>`_, `рефакторингом <http://ru.wikipedia.org/wiki/Рефакторинг>`_, `TDD <http://ru.wikipedia.org/wiki/Разработка_через_тестирование>`_, `свободным ПО <http://ru.wikipedia.org/wiki/Свободное_программное_обеспечение>`_, пользовательскими интерфейсами, `юзабилити <http://ru.wikipedia.org/wiki/Юзабилити>`_. Слежу за новшествами в сфере веб-разработки.


Другие интересы и увлечения
===========================
Творчество, созидание, развитие. Семья. Путешествия, велосипед. Играю на бильярде, в футбол, в настольный теннис.

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
{% endmacro %}

{% block content %}{{ profile() }}{% endblock %}
