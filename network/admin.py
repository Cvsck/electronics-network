from django.contrib import admin
from django.utils.html import format_html
from network.models import NetworkNode, Product


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления узлами сети.

    Возможности:
        - Отображение ключевых полей в списке объектов
        - Фильтрация по названию города, стране, поставщику
        - Поиск по названию, email, городу, стране
        - Отображение поставщика в виде кликабельной ссылки
        - Действие администратора: обнуление задолженности перед поставщиком
    """

    list_display = (
        "name",
        "role",
        "city",
        "country",
        "email",
        "supplier_link",
        "debt",
        "created_at",
    )
    list_filter = ("city", "country", "role", "supplier")
    search_fields = ("name", "email", "city", "country")
    actions = ["clear_debt"]

    @admin.display(description="Поставщик", ordering="supplier__name")
    def supplier_link(self, obj):
        """
        Возвращает HTML-ссылку на карточку поставщика, если он указан.
        """
        if obj.supplier:
            return format_html(
                '<a href="/admin/network/networknode/{}/change/">{}</a>',
                obj.supplier.id,
                obj.supplier.name,
            )
        return "-"

    @admin.action(description="Очистить задолженность перед поставщиком")
    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0.00)
        self.message_user(request, f"Задолженность обнулена у {updated} узлов.")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления товарами.

    Возможности:
        - Отображение ключевых полей: название, модель, цена, доступность
        - Фильтрация по доступности, узлу сети, дате выхода
        - Поиск по названию и модели
    """

    list_display = (
        "name",
        "model",
        "release_date",
        "price",
        "available",
        "network_node",
        "created_at",
    )
    list_filter = ("available", "release_date", "network_node")
    search_fields = ("name", "model")
