from datetime import datetime

import requests
from django.conf import settings
from django.http import Http404
from django_eventstream.viewsets import EventsViewSet
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Pattern, State
from .serializers import (
    EmptySerializer,
    PatternSerializer,
    StateSerializer,
    StateStartedSerializer,
    StateStoppedSerializer,
)


class PatternViewSet(viewsets.ModelViewSet):
    queryset = Pattern.objects.all()

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PatternSerializer
    pagination_class = None

    filterset_fields = ("enabled", "visible")
    search_fields = ("identifier", "name", "author", "school")
    ordering_fields = ("identifier", "name", "author", "school", "duration")

    lookup_field = "identifier"

    def create(self, request, *args, **kwargs):
        self.kwargs[self.lookup_field] = request.data[self.lookup_field]

        try:
            return self.update(request, *args, **kwargs)
        except Http404:
            return super().create(request, *args, **kwargs)

    @action(detail=True, methods=["post"], serializer_class=EmptySerializer)
    def enable(self, request, identifier=None):
        pattern = self.get_object()
        pattern.enabled = True
        pattern.save()

        return Response({"status": "Pattern enabled"})

    @action(detail=True, methods=["post"], serializer_class=EmptySerializer)
    def disable(self, request, identifier=None):
        pattern = self.get_object()
        pattern.enabled = False
        pattern.save()

        return Response({"status": "Pattern disabled"})

    @action(detail=True, methods=["post"], serializer_class=EmptySerializer)
    def run(self, request, identifier=None):
        requests.post(
            settings.RUNNER_URL,
            headers={"Authorization": f"Bearer {settings.RUNNER_TOKEN}"},
            params={"identifier": self.get_object().identifier},
        )

        return Response({"status": "Pattern run"})


class StateViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = StateSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(State.get_solo())
        return Response(serializer.data)

    @action(detail=False, methods=["post"], serializer_class=StateStartedSerializer)
    def started(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        state = State.get_solo()
        state.current_pattern = serializer.validated_data["pattern"]
        state.current_pattern_started = serializer.validated_data["started"]
        state.runner_last_active = datetime.now()
        state.save()

        return Response({"status": "OK"})

    @action(detail=False, methods=["post"], serializer_class=StateStoppedSerializer)
    def stopped(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        state = State.get_solo()
        state.current_pattern = None
        state.current_pattern_started = None
        state.runner_last_active = datetime.now()
        state.save()

        return Response({"status": "OK"})

    @action(detail=False, methods=["post"], serializer_class=EmptySerializer)
    def ping(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        state = State.get_solo()
        state.runner_last_active = datetime.now()
        state.save()

        return Response({"status": "OK"})


class EventStreamViewSet(EventsViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            channels=["runner"],
            messages_types=["message"],
        )
