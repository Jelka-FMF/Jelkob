from rest_framework import serializers

from ..models import Project, Submission


class ProjectSubmitSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field="shortid")

    class Meta:
        model = Submission

        fields = (
            "name",
            "description",
            "duration",
            "author",
            "school",
            "project",
        )
