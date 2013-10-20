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
    <title xml:lang="ru">naspeh</title>
    <atom:link type="application/atom+xml" href="{{ host }}{{ pages['/post.rss/'].url }}" rel="self"/>
    <link>{{ host }}</link>
    {#
    <pubDate>{{ site.time | date("%a, %d %b %Y %H:%M:%S %z") }}</pubDate>
    <lastBuildDate>{{ site.time | date("%a, %d %b %Y %H:%M:%S %z") }}</lastBuildDate>
    #}
    <language>ru-RU</language>
    <description>Статьи про linux, python, web</description>
    {% for page in pages['/post/'].children.values() %}
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
