from django.urls import path, include
from rest_framework.routers import DefaultRouter

from paint_company_project.paint_inventory.views import PaintViewSet


router = DefaultRouter(trailing_slash=False)
router.register(
    r"paints",
    PaintViewSet,
    basename="paints"
)

urlpatterns = [
    path('', include(router.urls)),
]