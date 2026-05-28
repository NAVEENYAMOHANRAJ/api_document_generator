from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("django-users", views.UserViewSet)

urlpatterns = [
    path("django-health/", views.health),
]
