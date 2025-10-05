from django.db import models
from django.utils import timezone


class NetworkNode(models.Model):
    """
    Узел сети электроники: завод, розничная сеть или ИП.
    """

    COUNTRY_CHOICES = [
        ("RU", "Россия"),
        ("UA", "Украина"),
        ("BY", "Беларусь"),
        ("KZ", "Казахстан"),
        ("GE", "Грузия"),
        ("AM", "Армения"),
        # добавь любые другие
    ]
    name = models.CharField("Название", max_length=255)
    email = models.EmailField("Email")
    country = models.CharField("Страна", max_length=2, choices=COUNTRY_CHOICES)
    city = models.CharField("Город", max_length=100)
    street = models.CharField("Улица", max_length=100)
    house_number = models.CharField("Номер дома", max_length=20)
    supplier = models.ForeignKey(
        "self",
        verbose_name="Поставщик",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    debt = models.DecimalField("Задолженность", max_digits=12, decimal_places=2)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Узел сети"
        verbose_name_plural = "Узлы сети"

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Представляет товар, связанный с конкретным узлом сети.

    Поля:
        - name: название продукта
        - model: модель
        - release_date: дата выхода на рынок
        - price: цена с точностью до копеек
        - available: доступность
        - network_node: узел сети, к которому привязан товар
        - created_at: время создания (устанавливается автоматически)
    """

    name = models.CharField("Название продукта", max_length=255)
    model = models.CharField("Модель", max_length=255)
    release_date = models.DateField("Дата выхода на рынок")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, default=0)
    available = models.BooleanField("В наличии", default=True)
    network_node = models.ForeignKey(
        NetworkNode,
        verbose_name="Узел сети",
        on_delete=models.CASCADE,
        related_name="products",
    )
    created_at = models.DateTimeField(
        "Время создания", auto_now_add=True
    )  # ✅ только auto_now_add

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.network_node.name})"
