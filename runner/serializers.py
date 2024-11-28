from rest_framework import serializers

from .models import Config, Pattern, State


class EmptySerializer(serializers.Serializer):
    pass


class PatternSerializer(serializers.ModelSerializer):
    changed = serializers.DateTimeField(source="history.first.history_date", read_only=True)

    class Meta:
        model = Pattern

        fields = (
            "identifier",
            "name",
            "description",
            "source",
            "docker",
            "duration",
            "author",
            "school",
            "changed",
            "enabled",
            "visible",
        )

    def to_representation(self, obj):
        ret = super().to_representation(obj)

        if obj.duration is None:
            ret["duration"] = Config.get_solo().default_duration

        return ret


class StateSerializer(serializers.ModelSerializer):
    currentPatternIdentifier = serializers.SlugRelatedField(source="current_pattern", slug_field="identifier", read_only=True)  # fmt: skip
    currentPatternStarted = serializers.DateTimeField(source="current_pattern_started")
    currentPatternRemaining = serializers.FloatField(source="current_pattern_remaining")
    runnerLastActive = serializers.DateTimeField(source="runner_last_active")
    runnerIsActive = serializers.BooleanField(source="runner_is_active")

    class Meta:
        model = State

        fields = (
            "currentPatternIdentifier",
            "currentPatternStarted",
            "currentPatternRemaining",
            "runnerLastActive",
            "runnerIsActive",
        )


class StateStartedSerializer(serializers.Serializer):
    pattern = serializers.SlugRelatedField(queryset=Pattern.objects.all(), slug_field="identifier")
    started = serializers.DateTimeField()


class StateStoppedSerializer(serializers.Serializer):
    pass
