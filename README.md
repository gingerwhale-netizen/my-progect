# Test-Bank API — автотесты

Автотесты к API банковского приложения.

**Стек:** Python, pytest, requests, pydantic, Allure, SQLAlchemy (PostgreSQL).

## Покрытие
- **Пользователи:** создание, авторизация
- **Счета:** создание, пополнение (`/deposit`), перевод (`/transfer`)
- **Кредиты:** запрос (`/credit/request`), погашение (`/credit/repay`)
- Проверки сохранения операций в **БД** (PostgreSQL) через SQLAlchemy
- Отчётность **Allure**

На каждую ручку — позитивный и негативный тест.

## Запуск
```bash
pip install pytest requests allure-pytest pydantic sqlalchemy psycopg2-binary rstr
pytest
```

Доступ к БД (для проверок): `localhost:5432`, база `symfony_db`, пользователь `symfony`.
