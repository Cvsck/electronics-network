from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, viewsets

from .models import NetworkNode, Product
from .permissions import IsActiveStaff
from .serializers import NetworkNodeSerializer, ProductSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    Управление узлами сети электроники.
    """

    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveStaff]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["country", "role", "supplier"]
    search_fields = ["name"]
    ordering_fields = ["created_at", "debt"]
    ordering = ["-created_at"]

    @extend_schema(description="Получить список всех узлов сети")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(description="Получить данные конкретного узла по ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(description="Создать новый узел сети")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(description="Полностью обновить узел сети по ID")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(description="Частично обновить узел сети по ID")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(description="Удалить узел сети по ID")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        """Обновление узла сети. Поле `debt` защищено от изменений."""
        validated_data = serializer.validated_data
        if "debt" in validated_data:
            validated_data.pop("debt")
        serializer.save()


class ProductViewSet(viewsets.ModelViewSet):
    """
    Управление товарами, связанными с узлами сети.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["available", "price", "network_node"]

    @extend_schema(description="Получить список всех товаров")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(description="Получить данные конкретного товара по ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(description="Создать новый товар")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(description="Полностью обновить товар по ID")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(description="Частично обновить товар по ID")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(description="Удалить товар по ID")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
