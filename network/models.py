from django.db import models


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
        # можно добавить другие страны
    ]

    ROLE_CHOICES = [
        ("factory", "Завод"),
        ("retail", "Розничная сеть"),
        ("individual", "Индивидуальный предприниматель"),
    ]

    name = models.CharField(
        "Название", max_length=255, unique=True
    )  # Уникальное название
    email = models.EmailField("Email", unique=True)  # Уникальный email
    country = models.CharField("Страна", max_length=2, choices=COUNTRY_CHOICES)
    role = models.CharField(
        "Тип узла", max_length=20, choices=ROLE_CHOICES, default="retail"
    )
    city = models.CharField("Город", max_length=100)
    street = models.CharField("Улица", max_length=100)
    house_number = models.CharField("Номер дома", max_length=20)
    supplier = models.ForeignKey(
        "self",
        verbose_name="Поставщик (предыдущий по иерархии объект сети)",
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

    def get_level(self) -> int:
        """
        Вычисляет уровень узла в иерархии:
        - 0: если нет поставщика (завод)
        - 1: если поставщик — завод
        - 2: если поставщик — магазин и т.д.
        """
        level = 0
        current = self
        while current.supplier:
            level += 1
            current = current.supplier
        return level


class Product(models.Model):
    """
    Представляет товар, связанный с конкретным узлом сети.
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
    created_at = models.DateTimeField("Время создания", auto_now_add=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.network_node.name})"
