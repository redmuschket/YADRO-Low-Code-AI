# Notification Service

Сервис для отправки уведомлений (email, SMS, Telegram) через очередь задач Celery с сохранением статусов в PostgreSQL.  
Построен на Flask + Celery + RabbitMQ + PostgreSQL.

## Стек технологий
- **Python 3.11**
- **Flask** (веб-фреймворк)
- **Celery** (очередь задач)
- **RabbitMQ** (брокер сообщений)
- **PostgreSQL** (хранение уведомлений)
- **SQLAlchemy** + Alembic (ORM и миграции)
- **Pydantic** (валидация запросов/ответов)
- **Gunicorn** (сервер)
- **Docker / Docker Compose** (контейнеризация)

## Структура проекта

<details><summary><b>Детальная структура:</b></summary>

```bash
notification-service/
├── app/                                                    # Основное приложение Flask
│   ├── __init__.py                                         # Фабрика create_app(), инициализация БД, middleware, blueprints
│   ├── http/                                               # HTTP-слой – контроллеры, middleware, маршруты, модели
│   │   ├── __init__.py
│   │   ├── controllers/                                    # Контроллеры (бизнес-логика запросов)
│   │   │   └── ...
│   │   ├── middleware/                                     # Промежуточные слои (middleware)
│   │   │   ├── database.py                                 # Открытие/закрытие сессии БД на каждый запрос
│   │   │   └── dependencies.py                             # Внедрение зависимостей (репозитории, сервисы) в g
│   │   ├── request_model/                                  # Pydantic-схемы входящих запросов
│   │   │   └── ...                            
│   │   ├── response_model/                                 # Pydantic-схемы исходящих ответов
│   │   │   └── ...                           
│   │   └── route/                                          # Регистрация маршрутов Flask
│   │       └── notification.py                             # URL-правила (POST, GET/<id>) с декораторами
│   └── service/                                            # Бизнес-логика и работа с данными
│       ├── base_repository.py                              # Базовый класс репозитория (общая логика)
│       ├── base_async_repository.py                        # Базовый асинхронный репозиторий (для Celery)
│       ├── base_sync_repository.py                         # Базовый синхронный репозиторий (для Flask)
│       └── notification/                                   # Сервисы уведомлений
│           ├── ...
│           └── processor/                                  # Процессоры отправки уведомлений
│               ├── send.py                                 # GetWay процессор отправки
│               └── ...
├── core/                                                   # Ядро приложения (общие компоненты)
│   ├── __init__.py                                         # Загрузка конфигурации и логгера
│   ├── http_status.py                                      # HTTP-статусы (константы)
│   ├── data_mapper/                                        # Преобразование типов
│   │   └── ...                                
│   ├── db/                                                 # База данных
│   │   ├── async_db.py                                     # Асинхронный движок и сессии (asyncpg)
│   │   ├── base.py                                         # Декларативная база SQLAlchemy (Base)
│   │   ├── config_db.py                                    # Конфигурация подключения к БД (ConfigDB)
│   │   ├── mixins.py                                       # Общие примеси для моделей
│   │   ├── sync_db.py                                      # Синхронный движок и сессии (psycopg2)
│   │   └── model/                                          # Модели SQLAlchemy
│   │       └── ...                           
│   ├── decorators/                                         # Декораторы
│   │   ├── api_router.py                                   # @handle_exceptions – перехват и форматирование ошибок
│   │   ├── timed.py                                        # @timed – замер времени выполнения
│   │   └── transactional.py                                # @transactional – управление транзакциями
│   ├── dependencies/                                       # Фабрики DI
│   │   ├── dependencies.py                                 # Общие зависимости
│   │   └── ...                                 
│   ├── domain/                                             # Доменные объекты
│   │   └── ...                               
│   ├── enum/                                               # Перечисления
│   │   └── ...
│   ├── exception/                                          # Кастомные исключения
│   │   └── ...
│   ├── logger/                                             # Система логирования
│   │   ├── logger.py                                       # Класс Logger (синглтон, настройка handler'ов)
│   │   └── logger_config.py                                # Конфигурация логирования (LoggerConfig)
│   │
│   └── utils/                                              # Утилиты
│       └── ...
├── workers/                                                # Фоновые задачи Celery
│   ├── celery_app.py                                       # Приложение Celery (конфигурация, брокер)
│   ├── dependencies.py                                     # Зависимости для воркеров
│   └── tasks/                                              # Задачи
│       └── ...
├── f_alembic/                                              # Миграции базы данных (Alembic)
│   ├── alembic.ini                                         # Конфигурация Alembic
│   ├── env.py                                              # Окружение миграций (подключение, metadata)
│   ├── script.py.mako                                      # Шаблон новых миграций
│   └── versions/                                           # Файлы миграций
│       └── ...
├── logs/                                                   # Файлы логов (автосоздание) появляются при работе в не докера 
│   ├── system_debug.log                                    
│   ├── system_errors.log                                   
│   ├── system_info.log                                     
│   └── user.log                                            
├── scripts/                                                # Вспомогательные скрипты
├── test/                                                   # Тесты
│   └── ...
├── .dockerignore                                           # Игнорируемые файлы Docker
├── .env.example                                            # Шаблон переменные окружения
├── .gitignore                                              # Игнорируемые файлы Git
├── config.yaml                                             # Конфигурация приложения (логи, БД)
├── config.py                                               # Класс Config (загрузка YAML + .env)
├── Dockerfile                                              # Инструкция сборки Docker-образа
├── docker-compose.yml                                      # Сервисы: flask-app, celery-worker, postgres, rabbitmq
├── gunicorn.conf.py                                        # Настройки Gunicorn (воркеры, hijack_root_logger)
├── main.py                                                 # Точка входа (локальный запуск)
├── README.md                                               # Документация проекта
└── requirements.txt                                        # Зависимости Python
```

</details>

## Установка и запуск

### Предварительные требования
- Docker и Docker Compose
- Python +3.11 (для локальной разработки)
- PostgreSQL и RabbitMQ (если запускаете без Docker)

### 1. Клонирование репозитория
```bash
git clone https://github.com/redmuschket/YADRO-Low-Code-AI.git
cd YADRO-Low-Code-AI
```

### 2. Конфигурация
- Перименовать .env.example в .env
- Указать RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASSWORD
- Указать POSTGRES_USERNAME, POSTGRES_PASSWORD

### 3. Запуск через Docker
```bash
docker-compose up -d --build
```

### Эта команда запустит:
- PostgreSQL
- RabbitMQ
- Flask
- Celery

## Локальный запуск (без Docker)

### Установите зависимости:
```bash
pip install -r requirements.txt
```

### Запустите PostgreSQL и RabbitMQ локально.
Примените миграции:
```bash
alembic -c f_alembic/alembic.ini upgrade head
```
### Запустите Flask (разработка):
```bash
python main.py
```

### В другом терминале запустите воркер Celery:
```bash
celery -A workers.celery_app worker --loglevel=info
```

## API Endpoints
### Создать уведомление
```bash
POST /api/v1/notifications/
Content-Type: application/json

{
  "type": "email",
  "recipient": "user@example.com",
  "message": "Test notification message"
}
```

Успешный ответ (202):
```bash
{
  "id": "019e29ee-8e8b-7a7e-89d8-d1876b44589e",
  "status": "queued"
}
```

### Получить уведомление по ID
```bash
http
GET /api/v1/notifications/{notification_id}
```

Ответ (200):
```bash
json
{
  "id": "019e29ee-8e8b-7a7e-89d8-d1876b44589e",
  "status": "sent"
}
```
### Проверка статуса (тот же эндпоинт)
Используйте GET-запрос с ID, чтобы узнать текущий статус (pending, processing, sent, failed).

## Логирование
### Логи разделены на системные (по уровням) и пользовательские.

Системные:
```bash
logs/system_info.log – INFO # (только информационные)

logs/system_errors.log – ERROR # и выше

logs/system_debug.log – DEBUG # (если включён debug)

Пользовательские: logs/user.log # (бизнес-события)
```

Формат логов настраивается в config.yaml.
### Для записи в пользовательский лог используйте:
```bash
from core import logger
logger_user = logger.get_logger('user')
user_logger.info("Сообщение")
```

## Миграции (Alembic)
Миграции лежат в f_alembic/versions/.
При старте Docker-контейнера миграции применяются автоматически (если включена переменная RUN_MIGRATIONS).

### Ручное создание миграции:

```bash
alembic -c f_alembic/alembic.ini revision --autogenerate -m "описание"
```

Применение:

```bash
alembic -c f_alembic/alembic.ini upgrade head
```
Если база недоступна локально, можно создать пустую миграцию и заполнить её вручную (см. документацию Alembic).

## Воркеры Celery
Задачи отправки уведомлений выполняются асинхронно.
При создании уведомления в очередь ставится задача, которая:

берёт запись из БД,

отправляет уведомление (email, SMS, Telegram),

обновляет статус (sent или failed).

## Тестирование

### Unit-test
<details> <summary><b>Linux / macOS</b></summary>

```bash
source .venv/bin/activate
```
</details><details> <summary><b>Windows</b></summary>

```bash
.venv\Scripts\Activate.ps1
```
</details>

```bash
pytest test/ -v
```

### Console
<details> <summary><b>Linux / macOS</b></summary>

```bash
curl -X POST http://localhost:5000/api/v1/notifications/ \
  -H "Content-Type: application/json" \
  -d '{
    "type": "email",
    "recipient": "user@example.com",
    "message": "Test notification message"
  }'
```

</details><details> <summary><b>Windows (PowerShell)</b></summary>

```powershell
Invoke-WebRequest -Uri http://localhost:5000/api/v1/notifications/ `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"type": "email", "recipient": "user@example.com", "message": "Test notification message"}'
```
</details>


## Примечания
- UUID7 генерируется с помощью библиотеки uuid6.
- Валидация входных данных через Pydantic (типы, формат email/телефона/Telegram).
- Все операции записи обёрнуты в транзакции (@transactional).
- Ошибки обрабатываются декоратором @handle_exceptions и возвращают JSON.
- Gunicorn настроен без перехвата логов (worker_hijack_root_logger = False), чтобы сохранить файловое логирование.