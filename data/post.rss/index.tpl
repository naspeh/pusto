<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:wfw="http://wellformedweb.org/CommentAPI/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
  xmlns:slash="http://purl.org/rss/1.0/modules/slash/"
  >
<channel>
    {% set root=pages['/post/'] %}
    <title xml:lang="ru">{{ root.title }}</title>
    <atom:link type="application/atom+xml" href="{{ host }}{{ pages['/post.rss/'].url }}" rel="self"/>
    <link>{{ host }}</link>
    <language>ru-RU</language>
    {% for page in root.children.values() %}
    <item>
        <title>{{ page.title | striptags }}</title>
        <link>{{ host }}{{ page.url }}</link>
        <pubDate>{{ page.published.strftime('%a, %d %b %Y %H:%M:%S %z') }}</pubDate>
        <dc:creator>naspeh</dc:creator>
        <description><![CDATA[ {{ page.body }} ]]></description>
    </item>
    {% endfor %}
</channel>
</rss>
