# -*- coding: utf-8 -*-
import re


RU = (
    u'ёыъэ',
    u'а,a;б,b;в,v;г,g;д,d;е,e;ё,yo;ж,zh;з,z;и,i;'
    u'й,y;к,k;л,l;м,m;н,n;о,o;п,p;р,r;с,s;т,t;'
    u'у,u;ф,f;х,h;ц,c;ч,ch;ш,sh;щ,shh;ъ,\";ы,y;ь,\';'
    u'э,e;ю,yu;я,ya'
)

UA = (
    u'єіїґ',
    u'а,a;б,b;в,v;г,g;ґ,g\';д,d;е,e;є,ye;ж,zh;з,z;'
    u'и,y;і,i;ї,i\';й,j;к,k;л,l;м,m;н,n;о,o;п,p;'
    u'р,r;с,s;т,t;у,u;ф,f;х,h;ц,c;ч,ch;ш,sh;щ,shh;'
    u'ь,\';ю,yu;я,ya'
)

ALL = {'ru': RU, 'ua': UA}

PRIORITY = ['ru', 'ua']


def is_unicode(text):
    if not isinstance(text, unicode):
        raise ValueError('Must be unicode')


def solve_langs(text, priority=PRIORITY):
    u'''
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
    >>> solve_langs('42')
    Traceback (most recent call last):
    ...
    ValueError: Must be unicode
    '''
    is_unicode(text)
    langs = []
    for lang in priority:
        pattern = ur'[%s]' % ALL[lang][0]
        if re.search(pattern, text):
            langs.append(lang)
    return langs and langs or [priority[0]]


def translify(text, langs=[], priority=PRIORITY):
    u'''
    >>> translify(u'хліб + сыр + масло = бутерброд')
    u'hlib + syr + maslo = buterbrod'
    >>> translify(u'хліб + сыр + масло = бутерброд', priority=['ua', 'ru'])
    u'hlib + syr + maslo = buterbrod'
    >>> translify(u'хлеб + масло = бутерброд', priority=['ua', 'ru'])
    u'hleb + maslo = buterbrod'
    >>> translify(u'хліб + сыр + масло = бутерброд', ['ua'])
    u'hlib + s\\u044br + maslo = buterbrod'
    >>> translify(u'хліб + сыр + масло = бутерброд', ['ru'])
    u'hl\\u0456b + syr + maslo = buterbrod'
    >>> translify(u'хліб + сыр + масло = бутерброд', ['ru', 'ua'])
    u'hlib + syr + maslo = buterbrod'
    >>> translify(u'съешь печенье')
    u's"esh\\' pechen\\'e'
    >>> translify('42')
    Traceback (most recent call last):
    ...
    ValueError: Must be unicode
    '''
    is_unicode(text)
    langs = langs and langs or solve_langs(text, priority)
    abc = ';'.join(ALL[lang][1] for lang in langs)
    for letter in abc.split(';'):
        letter = letter.split(',')
        text = text.replace(letter[0], letter[1])
        text = text.replace(letter[0].capitalize(), letter[1].capitalize())
    return text


def slugify(text):
    u'''
    >>> slugify(u'хліб + сыр + масло = бутерброд')
    u'hlib-syr-maslo-buterbrod'
    >>> slugify(u'Хлеб всему голова.')
    u'hleb-vsemu-golova'
    >>> slugify(u'съешь печенье')
    u's-esh-pechene'
    >>> slugify(42)
    Traceback (most recent call last):
    ...
    ValueError: Must be unicode
    '''
    text = translify(text)
    text = re.sub(r'[\']', '', text)
    text = re.sub(r'[^a-z0-9]+', '-', text.lower())
    return text.strip('-')
