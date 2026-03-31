from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class FrontendPagesSitemap(Sitemap):
    def items(self):
        return ["patterns", "about", "contact", "interaction"]

    def location(self, item):
        return reverse(item)
