mongokit
========
Если в node.parent запустить самого себя, то

::
    RuntimeError: maximum recursion depth exceeded


mongoengine
===========
- Не работает индекс node(parent, slug), требует parent в любом случае

- Если использовать choices в поле, то валидация отджельного поля не учитывает 
эти choices.
