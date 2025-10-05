"""
Маршруты проекта electronics-network.

Содержит:
    - Админ-панель Django: /admin/
    - REST API, сгенерированное через DRF Router: /api/

Router:
    Используется DefaultRouter от DRF для автоматической генерации CRUD-маршрутов:
        - /api/networknodes/ — управление узлами сети
        - /api/products/ — управление товарами

ViewSets:
    - NetworkNodeViewSet: обработка узлов сети
    - ProductViewSet: обработка товаров
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from network.views import NetworkNodeViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"networknodes", NetworkNodeViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]

"""
Маршруты для автогенерации и отображения OpenAPI-документации проекта.

Используется библиотека drf-spectacular для генерации схемы и Swagger-интерфейса.

Эндпоинты:
    - /api/schema/ — возвращает OpenAPI-схему в формате JSON
    - /api/docs/ — интерактивная Swagger-документация на основе схемы

Назначение:
    - Позволяет разработчикам и интеграторам видеть структуру API
    - Упрощает тестирование и интеграцию с фронтендом или внешними системами
"""

urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
