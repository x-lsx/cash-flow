# Движение денежных средств

## Обзор

Приложение предназначено для записи денежных операций (транзакций) с привязкой к типу (доход/расход), категории и подкатегории. Есть статус транзакции, комментарий и сумма. Админка предоставляет удобные фильтры по датам, категориям и подкатегориям.
## Структура проекта (важные файлы)

- `manage.py` — стандартная точка входа для управления Django-проектом.

- `config/settings.py` — настройки проекта (подключаемые приложения, БД и т.д.).

- `apps/cash_flow/models.py` — модели приложения.

- `apps/cash_flow/admin.py` — кастомизация Django Admin для удобной работы с моделями.

- `apps/cash_flow/migrations/` — миграции

- `databases/flow.db` — SQLite база данных (содержит данные проекта).

## Установка и запуск

### Клонирование репозитория
```
git clone <repository-url>
cd <project-directory>
```
### Windows

```powershell
# создаем вирутальное окружение
python -m venv .venv
# активируем вирутальное окружение
.\.venv\Scripts\Activate
# устанавилваем зависимости
pip install -r requirements.txt
```
### Linux/macOS

```powershell
# создаем вирутальное окружение
python3 -m venv .venv
# активируем вирутальное окружение
source .venv/bin/activate
# устанавливаем зависимости
pip install -r requirements.txt
```
## Запуск локально:

```powershell

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

```

#### Откройте http://127.0.0.1:8000/admin и войдите под суперпользователем.

## Модели

Файл: `apps/cash_flow/models.py`.

1) FlowStatus
- Поля: `name` (CharField, max_length=50)
- Представление: `__str__` возвращает имя.

2) FlowType
- Поля: `name` (CharField, max_length=50)
- Представление: `__str__` возвращает имя.

3) FlowCategory
- Поля: `name` (CharField, max_length=50), `type` (ForeignKey -> FlowType)
- `__str__` возвращает название категории.

4) FlowSubcategory
- Поля: `name` (CharField, max_length=50), `category` (ForeignKey -> FlowCategory)
- `__str__` возвращает название подкатегории.

5) Transaction
- Поля:
  - `status` (ForeignKey -> FlowStatus)
  - `type` (ForeignKey -> FlowType)
  - `category` (ChainedForeignKey -> FlowCategory)
  - `subcategory` (ChainedForeignKey -> FlowSubcategory)
  - `amount` (DecimalField, max_digits=10, decimal_places=2)
  - `comment` (TextField, null=True, blank=True)
  - `created_at` (DateField, default=timezone.now)
- Метод `clean` проверяет, что `amount` > 0, иначе выбрасывает `ValidationError`.
- `__str__` выводит дату и сумму в рублях.

## Админ-интерфейс

Файл: `apps/cash_flow/admin.py`.

- Определены два кастомных фильтра `UniqueCategoryListFilter` и `UniqueSubcategoryListFilter`, которые показывают уникальные значения `name` категорий и подкатегорий соответственно.
- `FlowStatusAdmin`, `FlowTypeAdmin` — простые admin.ModelAdmin с `list_display` и `search_fields`.
- `FlowCategoryAdmin` — отображает `name` и `type`, фильтры по `name` и `type`.
- `FlowSubcategoryAdmin` — фильтры по `name` и по `category` (через `UniqueCategoryListFilter`).
- `TransactionAdmin` — показывает `created_at`, `amount`, `status`, `type`, `category`, `subcategory`, `comment`. Фильтры: диапазон дат (`DateRangeFilter`), `status`, `type` и кастомные уникальные фильтры по категориям и подкатегориям. `date_hierarchy` установлен на `created_at`.

## Внешние библиотеки

- smart_selects — позволяет создавать зависимые поля в админке (ChainedForeignKey). ChainedForeignKey: используется `smart_selects.db_fields.ChainedForeignKey` для динамической фильтрации категорий/подкатегорий в админке.
- rangefilter — предоставляет `DateRangeFilter` для админки.