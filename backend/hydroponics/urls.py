from django.urls import include, path
from rest_framework import routers

from hydroponics.views import HydroponicSystemView, MeasurementView

router = routers.DefaultRouter()
router.register("", HydroponicSystemView, "hydroponic_system")

urlpatterns = [
    path(
        "<int:hydroponics_id>/measurements",
        MeasurementView.as_view(),
        name="measurements",
    ),
    path("", include(router.urls)),
]
