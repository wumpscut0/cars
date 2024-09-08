from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from .views import (
    index,
    UserCreateView,
    CarModelViewSet,
    CarDetailView,
    CarListView,
    CarCreateView,
    CarUprateView,
    CarDeleteView,
)

app_name = "carsapp"

router = DefaultRouter()
router.register(r"cars", CarModelViewSet, basename="cars")

urlpatterns = [
    path("", index, name="index"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="carsapp/login.html"), name="login"),
    path(
        "logout/",
        LogoutView.as_view(template_name="carsapp/logout.html"),
        name="logout",
    ),
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("api/", include(router.urls)),
    path("cars/", CarListView.as_view(), name="car_list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car_detail"),
    path("cars/<int:pk>/update", CarUprateView.as_view(), name="car_update"),
    path("cars/<int:pk>/delete", CarDeleteView.as_view(), name="car_delete"),
    path("cars/create/", CarCreateView.as_view(), name="car_create"),
]
