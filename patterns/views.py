from datetime import datetime

from django.http import Http404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Pattern, State
from .serializers import (
    PatternSerializer,
    StatePingSerializer,
    StateSerializer,
    StateStartedSerializer,
    StateStoppedSerializer,
)


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


class StateViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = StateSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(State.get_solo())
        return Response(serializer.data)

    @action(detail=False, methods=["post"], serializer_class=StateStartedSerializer)
    def started(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        state = State.get_solo()
        state.pattern = serializer.validated_data["pattern"]
        state.started = serializer.validated_data["started"]
        state.active = datetime.now()
        state.save()

        return Response({"status": "OK"})

    @action(detail=False, methods=["post"], serializer_class=StateStoppedSerializer)
    def stopped(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        state = State.get_solo()
        state.pattern = None
        state.started = None
        state.active = datetime.now()
        state.save()

        return Response({"status": "OK"})

    @action(detail=False, methods=["post"], serializer_class=StatePingSerializer)
    def ping(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        state = State.get_solo()
        state.active = datetime.now()
        state.save()

        return Response({"status": "OK"})
