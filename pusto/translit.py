# -*- coding: utf-8 -*-
import re


RU = (
    u'ёыъэ',
    u'а,a;б,b;в,v;г,g;д,d;е,e;ё,yo;ж,zh;з,z;и,i;'
    u'й,y;к,k;л,l;м,m;н,n;о,o;п,p;р,r;с,s;т,t;'
    u'у,u;ф,f;х,kh;ц,c;ч,ch;ш,sh;щ,shch;ъ,\";ы,y;ь,\';'
    u'э,e;ю,yu;я,ya'
)

UA = (
    u'єіїґ',
    u'а,a;б,b;в,v;г,g;ґ,g\';д,d;е,e;є,je;ж,zh;з,z;'
    u'и,y;і,i;ї,i\';й,j;к,k;л,l;м,m;н,n;о,o;п,p;'
    u'р,r;с,s;т,t;у,u;ф,f;х,h;ц,c;ч,ch;ш,sh;щ,shh;'
    u'ь,\';ю,ju;я,ja'
)

ALL = {'ru': RU, 'ua': UA}

PRIORITY = ['ru', 'ua']


def is_unicode(text):
    if not isinstance(text, unicode):
        raise ValueError('Must be unicode')


def solve_langs(text, priority=PRIORITY):
    is_unicode(text)
    langs = []
    for lang in priority:
        pattern = ur'[%s]' % ALL[lang][0]
        if re.search(pattern, text):
            langs.append(lang)
    return langs and langs or [priority[0]]


def translify(text, langs=[], priority=PRIORITY):
    is_unicode(text)
    langs = langs and langs or solve_langs(text, priority)
    abc = ';'.join(ALL[lang][1] for lang in langs)
    for letter in abc.split(';'):
        letter = letter.split(',')
        text = text.replace(letter[0], letter[1])
        text = text.replace(letter[0].capitalize(), letter[1].capitalize())
    return text


def slugify(text):
    text = translify(text)
    return re.sub('[^a-z0-9]+', '-', text.lower()).strip('-')
