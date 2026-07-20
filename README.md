# API Key Manager

REST API для управления клиентами и API-ключами.

Сервис позволяет выпускать, отзывать и проверять API-ключи, а также ограничивать доступ к эндпоинтам с помощью scope.

## Демо

API:
https://api-key-manager.piksi.dev

Swagger:
https://api-key-manager.piksi.dev/docs

## Возможности

- создание клиентов;
- выпуск API-ключей;
- отзыв API-ключей;
- проверка срока действия;
- проверка scope;
- хранение только SHA-256 хэша ключей.

## Технологии

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- Alembic
- Pydantic
- uv
- Docker
- GitHub Actions
- Cloud.ru Container Apps
- pytest

## Безопасность

API-ключ отображается только один раз при создании.

В базе данных хранится только SHA-256 хэш ключа.

Для доступа к защищённым эндпоинтам используется заголовок:

```http
X-API-Key: <raw_key>
```

Ключ считается недействительным, если:

- не существует;
- был отозван;
- истёк срок действия.

## Локальный запуск

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn main:app --reload
```

### Переменные окружения

```env
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>:5432/<database>
```

Для локального запуска требуется доступная PostgreSQL-база данных.

## Тесты

```bash
uv run pytest
```

## Deployment

Проект контейнеризирован с помощью Docker.

При публикации изменений GitHub Actions:

- собирает Docker-образ;
- публикует его в Artifact Registry.

Cloud.ru Container Apps автоматически обнаруживает новый образ и разворачивает обновлённую версию приложения.
