from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from ml_api.views import EndpointViewSet, RequestViewSet, AlgorithmViewSet, PredictView

router = DefaultRouter(trailing_slash=False)

router.register(r"endpoints", EndpointViewSet, basename="endpoints")
router.register(r"algorithms", AlgorithmViewSet, basename="algorithms")
router.register(r"requests", RequestViewSet, basename="requests")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    re_path(r"^api/v1/(?P<endpoint_name>.+)/predict$", PredictView.as_view(), name="predict"),
]

