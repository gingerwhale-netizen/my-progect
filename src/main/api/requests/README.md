# Пакет `requests/` — устаревший слой реквестеров

## Статус: не используется в текущих тестах

Это ранняя реализация HTTP-реквестеров «по одному классу на эндпоинт».
В актуальном коде она **не задействована**: шаги (`steps/*`) и тесты
работают через универсальный слой `foundation/requesters/`
(`CrudRequester` и `ValidateCrudRequester`), который конфигурируется
через `Endpoint` (см. `foundation/endpoint.py`).

Пакет оставлен как справочный / на случай возврата к подходу
«отдельный реквестер под каждый эндпоинт». Активной ссылки на него из
`steps`, `fixtures` или `test` нет.

## Состав пакета

| Файл | Класс | Назначение | Эндпоинт |
|---|---|---|---|
| `requester.py` | `Requester(ABC)` | Базовый абстрактный класс: хранит `request_spec` и `response_spec`, задаёт абстрактный `post()` | — |
| `create_user_requester.py` | `CreateUserRequester` | Создание пользователя | `POST /admin/create` |
| `login_user_requester.py` | `LoginUserRequester` | Логин пользователя | `POST /auth/token/login` |
| `create_account_requester.py` | `CreateAccountRequester` | Создание счета | `POST /account/create` |

## Чем отличается от `foundation/requesters/`

- **`requests/` (этот пакет):** отдельный класс под каждый эндпоинт,
  URL и модель ответа «зашиты» в самом классе.
- **`foundation/requesters/` (актуальный подход):** один универсальный
  `CrudRequester`/`ValidateCrudRequester`, а URL и модели берутся из
  конфигурации `Endpoint`. Именно он используется во всех шагах.

## Если решите удалить

Пакет можно безопасно удалить — на него нет внешних импортов
(только внутренние ссылки на `requester.Requester`). Перед удалением
достаточно убедиться, что `grep` по `requests.create_user_requester`,
`requests.login_user_requester`, `requests.create_account_requester`
и `requests.requester` не даёт совпадений вне самого пакета.
