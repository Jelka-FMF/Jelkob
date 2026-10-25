from .common import urlpatterns as common_urlpatterns
from .pxt import urlpatterns as pxt_urlpatterns
from .python import urlpatterns as python_urlpatterns

urlpatterns = [
    *common_urlpatterns,
    *pxt_urlpatterns,
    *python_urlpatterns,
]
