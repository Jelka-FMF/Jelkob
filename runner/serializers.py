from datetime import datetime

from rest_framework import serializers

from .models import Config, Pattern, State


class EmptySerializer(serializers.Serializer):
    pass


class PatternSerializer(serializers.ModelSerializer):
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
            "enabled",
            "visible",
        )

    def to_representation(self, obj):
        ret = super().to_representation(obj)

        if obj.duration is None:
            ret["duration"] = Config.get_solo().duration

        return ret


class StateSerializer(serializers.ModelSerializer):
    pattern = serializers.SlugRelatedField(slug_field="identifier", read_only=True)
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ("pattern", "started", "active", "remaining")

    @staticmethod
    def get_remaining(obj):
        if not obj.pattern or not obj.started:
            return 0

        duration = obj.pattern.duration or Config.get_solo().duration
        started = obj.started.timestamp()
        now = datetime.now().timestamp()

        return max(0, duration - (now - started))


class StateStartedSerializer(serializers.Serializer):
    pattern = serializers.SlugRelatedField(queryset=Pattern.objects.all(), slug_field="identifier")
    started = serializers.DateTimeField()


class StateStoppedSerializer(serializers.Serializer):
    pass
