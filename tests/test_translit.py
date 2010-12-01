# -*- coding: utf-8 -*-


def test():
    u'''
    NOTICE: Need Doctest

    >>> from pusto.translit import translify, slugify, solve_langs
    >>> solve_langs(u'сыр')
    ['ru']
    >>> solve_langs(u'хліб')
    ['ua']
    >>> solve_langs(u'хліб + сыр')
    ['ru', 'ua']
    >>> solve_langs(u'сыр', ['ua'])
    ['ua']
    >>> solve_langs(u'сыр', ['ua', 'ru'])
    ['ru']
    >>> translify(u'хліб + сыр + масло = бутерброд')
    u'khlib + syr + maslo = buterbrod'
    >>> translify(u'хліб + сыр + масло = бутерброд', priority=['ua', 'ru'])
    u'hlib + syr + maslo = buterbrod'
    >>> translify(u'хлеб + масло = бутерброд', priority=['ua', 'ru'])
    u'hleb + maslo = buterbrod'
    >>> translify(u'хліб + сыр + масло = бутерброд', ['ua'])
    u'hlib + s\\u044br + maslo = buterbrod'
    >>> translify(u'хліб + сыр + масло = бутерброд', ['ru'])
    u'khl\\u0456b + syr + maslo = buterbrod'
    >>> translify(u'хліб + сыр + масло = бутерброд', ['ru', 'ua'])
    u'khlib + syr + maslo = buterbrod'
    >>> slugify(u'хліб + сыр + масло = бутерброд')
    u'khlib-syr-maslo-buterbrod'
    >>> slugify(u'Хлеб всему голова.')
    u'khleb-vsemu-golova'
    >>> translify(u'хор', ['ua'])
    u'hor'
    >>> translify(u'хор', ['ru'])
    u'khor'
    >>> translify('42')
    Traceback (most recent call last):
    ...
    ValueError: Must be unicode
    >>> slugify(42)
    Traceback (most recent call last):
    ...
    ValueError: Must be unicode
    >>> solve_langs('42')
    Traceback (most recent call last):
    ...
    ValueError: Must be unicode
    '''
