from django.conf import settings
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.exceptions import NotFound

from ..models import PXTProject, Project, PythonProject


class ShareProject(generics.GenericAPIView):
    queryset = Project.objects.all()
    lookup_field = "ulid"

    def get(self, request, *args, **kwargs):
        project = self.get_object()

        if isinstance(project, PXTProject):
            url = f"{settings.JELKLY_EDITOR_URL}#{settings.JELKLY_EDITOR_ACTION}:{project.longid}"
        elif isinstance(project, PythonProject):
            url = f"{settings.JELKONDA_EDITOR_URL}#{settings.JELKONDA_EDITOR_ACTION}:{project.ulid}"
        else:
            raise NotFound("Unsupported project type.")

        return redirect(url)
