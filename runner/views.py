from abc import ABC
from datetime import datetime

from django.http import Http404
from django_eventstream import send_event
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
        data = {"identifier": self.get_object().identifier}
        send_event("control", "run", data)

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

        send_event(
            "status",
            "started",
            {
                "identifier": state.current_pattern.identifier,
                "started": state.current_pattern_started,
                "remaining": state.current_pattern_remaining,
            },
        )

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

        send_event("status", "stopped", None)

        return Response({"status": "OK"})

    @action(detail=False, methods=["post"], serializer_class=EmptySerializer)
    def ping(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        state = State.get_solo()
        state.runner_last_active = datetime.now()
        state.save()

        return Response({"status": "OK"})


class AbstractEventsViewSet(EventsViewSet, ABC):
    def get_renderers(self):
        # Skip custom logic that would disable renderers if custom default renderers are set
        return super(EventsViewSet, self).get_renderers()

    def list(self, request):
        # Disable selecting channels from query parameters
        return self._stream_or_respond(self.channels, request)

    def channel(self, request, channel=None):
        # Disable selecting channels from endpoint
        return None


class ControlEventsViewSet(AbstractEventsViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            channels=["control"],
            messages_types=["patterns", "run"],
        )


class StatusEventsViewSet(AbstractEventsViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            channels=["status"],
            messages_types=["status", "started", "stopped"],
        )
