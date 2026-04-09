from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class FrontendPagesSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return ["patterns", "about", "contact", "interaction"]

    def location(self, item):
        return reverse(item)
