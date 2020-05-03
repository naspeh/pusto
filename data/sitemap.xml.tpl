<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {% for page in p.pages.values() %}
    {% if page.url | match('^/($|(post|trip|s|naspeh|en|mailur)/)') and not page.url | match('.*/photos/.*') and page.index_file %}
    <url>
        <loc>{{ host }}{{ page.url }}</loc>
    </url>
    {% endif %}
    {% endfor %}
</urlset>
