# electronics-network (Электронная торговая сеть) — Django + DRF
# Архитектурно чистое веб-приложение для управления торговой сетью электроники.
'''
Реализована иерархия узлов (заводы, сети, ИП),
управление продуктами, задолженностью, API и административная панель.
'''
# 🚀 Стек технологий
'''
- Python 3.8+
- Django 3+
- Django REST Framework 3.10+
- PostgreSQL 10+
- django-filter
'''
# 🧱 Архитектура
'''
- Модель NetworkNode:
  - Название, контакты, поставщик, задолженность, дата создания
  - Иерархия через связь supplier
- Модель Product:
  - Название, модель, дата выхода, связь с узлом
- Админка:
  - Ссылка на поставщика
  - Фильтр по городу
  - Admin action: очистка задолженности
- API:
  - CRUD для узлов
  - Защита поля debt от изменения
  - Фильтрация по стране
  - Поиск по названию
  - Доступ только для активных сотрудников
'''
# 📦 Установка
'''
git clone https://github.com/Cvsck/electronics-network
cd electronics-network
poetry install
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
'''
# 🔐 Доступ к API
'''
Доступ разрешён только активным сотрудникам (`is_staff=True`, `is_active=True`).
'''
