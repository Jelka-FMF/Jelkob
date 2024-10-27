from django.http import Http404
from rest_framework import permissions, viewsets

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
