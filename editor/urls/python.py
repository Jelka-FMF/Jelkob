from django.urls import path, re_path

from ..views import PythonProjectView, PythonSubmitProjectView, PythonUploadProjectView

urlpatterns = [
    path(
        "python/upload",
        PythonUploadProjectView.as_view(),
        name="python-project-upload",
    ),
    path(
        "python/submit",
        PythonSubmitProjectView.as_view(),
        name="python-project-submit",
    ),
    re_path(
        r"^python/projects/(?P<ulid>[0-9A-HJKMNP-TV-Z]{26})$",
        PythonProjectView.as_view(),
        name="python-project-get",
    ),
]
