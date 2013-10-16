<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {% for page in pages.values() %}
    {% if not page.url | match('^/s/$|^/draft|^/sitemap\.xml/') %}
    <url>
        <loc>http://pusto.org{{ page.url }}</loc>
    </url>
    {% endif %}
    {% endfor %}
</urlset>
