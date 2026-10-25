from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response

from ..models import PythonProject, Submission
from ..serializers import (
    PythonProjectCreateSerializer,
    PythonProjectSerializer,
    PythonProjectSubmitSerializer,
)


class PythonProjectView(generics.RetrieveAPIView):
    queryset = PythonProject.objects.all()
    serializer_class = PythonProjectSerializer
    lookup_field = "ulid"


@method_decorator(csrf_exempt, name="dispatch")
class PythonUploadProjectView(generics.CreateAPIView):
    queryset = PythonProject.objects.all()
    serializer_class = PythonProjectCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = serializer.save()
        data = PythonProjectSerializer(project).data

        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


@method_decorator(csrf_exempt, name="dispatch")
class PythonSubmitProjectView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = PythonProjectSubmitSerializer
