from django.urls import path, include
from rest_framework.routers import DefaultRouter

from paint_company_project.user.views import UserViewSet


router = DefaultRouter(trailing_slash=False)
router.register(
    r"user",
    UserViewSet,
    basename="user"
)

urlpatterns = [
    path('', include(router.urls)),
]