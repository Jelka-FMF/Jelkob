from django.urls import get_resolver, reverse
from rest_framework.response import Response
from rest_framework.views import APIView


class APIRootView(APIView):
    def get(self, request, *args, **kwargs):
        urls = {}

        for resolver in get_resolver().url_patterns:
            if hasattr(resolver, "urlconf_module"):
                for pattern in getattr(resolver.urlconf_module, "urlpatterns", resolver.urlconf_module):
                    if hasattr(pattern, "url_patterns"):
                        for subpattern in pattern.url_patterns:
                            if subpattern.name and subpattern.name.endswith("-list"):
                                prefix = subpattern.name.split("-")[0]
                                urls[prefix] = request.build_absolute_uri(reverse(subpattern.name))

        return Response(urls)
