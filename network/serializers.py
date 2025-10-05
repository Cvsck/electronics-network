from rest_framework import serializers
from .models import NetworkNode, Product


class SupplierSerializer(serializers.ModelSerializer):
    """
    Вложенный сериализатор для отображения поставщика узла сети.
    Отображает только имя и город поставщика.
    """
    class Meta:
        model = NetworkNode
        fields = ("id", "name", "city")


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для узлов сети.

    Архитектурные особенности:
        - supplier: вложенный объект (только для чтения)
        - supplier_id: ID поставщика (для записи)
        - level: вычисляемый уровень узла
        - debt: только для чтения
    """

    supplier = SupplierSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(),
        source="supplier",
        write_only=True,
        required=False,
    )
    level = serializers.SerializerMethodField()

    def get_level(self, obj):
        return obj.get_level()

    class Meta:
        model = NetworkNode
        fields = (
            "id",
            "name",
            "email",
            "country",
            "role",
            "city",
            "street",
            "house_number",
            "supplier",
            "supplier_id",
            "level",
            "debt",
            "created_at",
        )
        read_only_fields = ("debt", "created_at", "level")


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Включает вложенный узел сети (NetworkNode) в виде объекта.
    """

    network_node = NetworkNodeSerializer(read_only=True)
    network_node_id = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(),
        source="network_node",
        write_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "model",
            "release_date",
            "price",
            "available",
            "network_node",
            "network_node_id",
        ]
