<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <id>{{ host }}{{ url }}</id>
    <link href="{{ host }}"/>
    <link href="{{ host }}{{ url }}" ref="self"/>
    <title>{{ title|striptags }}</title>
    <updated>{{ now | rfc3339 }}</updated>
    <author>
        <name>{{ author }}</name>
    </author>

    {% for page in children.values() %}
    <entry xml:base="{{ host }}{{ url }}">
        <title type="text">{{ page.title | striptags }}</title>
        <link href="{{ host }}{{ page.url }}"/>
        <id>{{ host}}{{ page.url }}</id>
        <updated>{{ page.published | rfc3339 }}</updated>
        <author>
            <name>{{ ', '.join(page.author or []) or author }}</name>
        </author>
        {% if shorten %}
        <summary><![CDATA[ {{ page.summary}} ]]></summary>
        {% else %}
        <content type="html"><![CDATA[ {{ page.body }} ]]></content>
        {% endif %}
    </entry>
    {% endfor %}
</feed>
