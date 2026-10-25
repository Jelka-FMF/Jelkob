from .common import urlpatterns as common_urlpatterns
from .pxt import urlpatterns as pxt_urlpatterns

urlpatterns = [
    *common_urlpatterns,
    *pxt_urlpatterns,
]
