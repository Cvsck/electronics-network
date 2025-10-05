from django.contrib import admin

from network.models import NetworkNode, Product


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления узлами сети.

    Возможности:
        - Отображение ключевых полей в списке объектов
        - Фильтрация по названию города
        - Отображение поставщика в виде кликабельной ссылки
        - Действие администратора: обнуление задолженности перед поставщиком
    """

    list_display = (
        "name",
        "city",
        "country",
        "email",
        "supplier_link",
        "debt",
        "created_at",
    )
    list_filter = ("city", "country", "supplier")
    search_fields = ("name", "email", "city", "country")
    actions = ["clear_debt"]

    def supplier_link(self, obj):
        """
        Возвращает HTML-ссылку на карточку поставщика, если он указан.
        """
        if obj.supplier:
            return f'<a href="/admin/network/networknode/{obj.supplier.id}/change/">{obj.supplier.name}</a>'
        return "-"

    supplier_link.allow_tags = True
    supplier_link.short_description = "Поставщик"

    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0.00)
        self.message_user(request, f"Задолженность обнулена у {updated} узлов.")

    clear_debt.short_description = "Очистить задолженность перед поставщиком"

    def get_actions(self, request):
        actions = super().get_actions(request)
        print("Доступные действия:", actions.keys())
        return actions


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
