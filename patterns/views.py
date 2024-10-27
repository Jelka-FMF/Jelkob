from django.http import Http404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Pattern
from .serializers import PatternSerializer


class PatternViewSet(viewsets.ModelViewSet):
    queryset = Pattern.objects.all()

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PatternSerializer
    pagination_class = None

    filterset_fields = ("enabled",)
    search_fields = ("identifier", "name", "author", "school")
    ordering_fields = ("identifier", "name", "author", "school", "duration")

    lookup_field = "identifier"

    def create(self, request, *args, **kwargs):
        self.kwargs[self.lookup_field] = request.data[self.lookup_field]

        try:
            return self.update(request, *args, **kwargs)
        except Http404:
            return super().create(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def enable(self, request, pk=None):
        pattern = self.get_object()
        pattern.enabled = True
        pattern.save()

        return Response({"status": "Pattern enabled"})

    @action(detail=True, methods=["post"])
    def disable(self, request, pk=None):
        pattern = self.get_object()
        pattern.enabled = False
        pattern.save()

        return Response({"status": "Pattern disabled"})

    @action(detail=True, methods=["post"])
    def run(self, request, pk=None):
        return Response({"status": "Not implemented yet"})
