from rest_framework import serializers

from .models import Pattern, State


class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ("identifier", "name", "docker", "duration", "author", "school", "enabled")


class StateSerializer(serializers.ModelSerializer):
    pattern = serializers.SlugRelatedField(slug_field="identifier", read_only=True)

    class Meta:
        model = State
        fields = ("pattern", "started", "active")


class StateStartedSerializer(serializers.Serializer):
    pattern = serializers.SlugRelatedField(queryset=Pattern.objects.all(), slug_field="identifier")
    started = serializers.DateTimeField()


class StateStoppedSerializer(serializers.Serializer):
    pattern = serializers.SlugRelatedField(queryset=Pattern.objects.all(), slug_field="identifier")


class StatePingSerializer(serializers.Serializer):
    pass
