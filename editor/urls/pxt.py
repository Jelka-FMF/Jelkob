from django.urls import path, re_path

from ..views import (
    PXTUploadProjectView,
    PXTProjectByLongIdView,
    PXTProjectByShortIdView,
    PXTProjectContentByLongIdView,
    PXTProjectContentByShortIdView,
    PXTShareProjectByLongIdView,
    PXTShareProjectByShortIdView,
    PXTSubmitProjectView,
)

urlpatterns = [
    re_path(
        r"^pxt/(?P<longid>\d{5}-\d{5}-\d{5}-\d{5})$",
        PXTProjectByLongIdView.as_view(),
        name="pxt-project-get-longid",
    ),
    re_path(
        r"^pxt/(?P<longid>\d{5}-\d{5}-\d{5}-\d{5})/text$",
        PXTProjectContentByLongIdView.as_view(),
        name="pxt-project-get-longid-content",
    ),
    re_path(
        r"^pxt/(?P<shortid>_\w{12})$",
        PXTProjectByShortIdView.as_view(),
        name="pxt-project-get-shortid",
    ),
    re_path(
        r"^pxt/(?P<shortid>_\w{12})/text$",
        PXTProjectContentByShortIdView.as_view(),
        name="pxt-project-get-shortid-content",
    ),
    path(
        "pxt/scripts",
        PXTUploadProjectView.as_view(),
        name="pxt-project-upload",
    ),
    path(
        "pxt/submit",
        PXTSubmitProjectView.as_view(),
        name="pxt-project-submit",
    ),
    re_path(
        r"^share/(?P<longid>\d{5}-\d{5}-\d{5}-\d{5})$",
        PXTShareProjectByLongIdView.as_view(),
        name="pxt-project-share-longid",
    ),
    re_path(
        r"^share/(?P<shortid>_\w{12})$",
        PXTShareProjectByShortIdView.as_view(),
        name="pxt-project-share-shortid",
    ),
]
