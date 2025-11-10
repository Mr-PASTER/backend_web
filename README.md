# Lever Control & Projects API

FastAPI приложение для управления рычагами и хранения информации о проектах.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

Запустите сервер с помощью uvicorn:

```bash
uvicorn main:app --reload --port 10000
```

Сервер будет доступен по адресу: http://localhost:10000

## Документация API

После запуска сервера доступна интерактивная документация:
- Swagger UI: http://localhost:10000/docs
- ReDoc: http://localhost:10000/redoc

## API Endpoints

### Рычаги (Levers)

- `POST /levers/` - Создать новый рычаг
- `GET /levers/` - Получить все рычаги
- `GET /levers/{lever_id}` - Получить рычаг по ID
- `PUT /levers/{lever_id}` - Обновить рычаг
- `PATCH /levers/{lever_id}/position` - Установить позицию рычага
- `PATCH /levers/{lever_id}/toggle` - Переключить состояние рычага
- `DELETE /levers/{lever_id}` - Удалить рычаг

### Проекты (Projects)

- `POST /projects/` - Создать новый проект с произвольным количеством изображений
- `GET /projects/` - Получить список проектов
- `GET /projects/{project_id}` - Получить проект по ID
- `PUT /projects/{project_id}` - Обновить данные проекта и список изображений
- `DELETE /projects/{project_id}` - Удалить проект

## Примеры использования

### Создание рычага
```bash
curl -X POST "http://localhost:10000/levers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Рычаг 1",
    "description": "Основной рычаг управления",
    "position": 50.0,
    "is_active": true
  }'
```

### Получение всех рычагов
```bash
curl "http://localhost:10000/levers/"
```

### Установка позиции рычага
```bash
curl -X PATCH "http://localhost:10000/levers/1/position?position=75.5"
```

### Переключение состояния рычага
```bash
curl -X PATCH "http://localhost:10000/levers/1/toggle"
```

### Создание проекта
```bash
curl -X POST "http://localhost:10000/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Новый сайт портфолио",
    "short_description": "Обновленная версия персонального сайта",
    "full_description": "Подробное описание проекта с технологиями и результатами.",
    "images": [
      "https://example.com/images/portfolio-home.png",
      "https://example.com/images/portfolio-about.png"
    ]
  }'
```

## Деплой

### Бесплатные варианты деплоя

#### Railway (Рекомендуется)
1. Зарегистрируйтесь на [Railway](https://railway.app)
2. Подключите GitHub репозиторий
3. Railway автоматически обнаружит Python проект и задеплойт его
4. API будет доступно по сгенерированному URL

#### Render
1. Зарегистрируйтесь на [Render](https://render.com)
2. Создайте новый Web Service
3. Подключите GitHub репозиторий
4. Укажите команду запуска: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### Fly.io
1. Установите flyctl: `curl -L https://fly.io/install.sh | sh`
2. `fly launch` в корне проекта
3. `fly deploy` для деплоя

## Структура проекта

```
backend/
├── app/
│   ├── __init__.py
│   ├── db.py              # Подключение к базе данных
│   ├── models.py          # Pydantic модели рычагов
│   ├── database.py        # Логика работы с рычагами (in-memory)
│   ├── projects/
│   │   ├── __init__.py
│   │   ├── models.py      # SQLAlchemy модели проектов и изображений
│   │   └── schemas.py     # Pydantic-схемы проектов
│   └── routers/
│       ├── __init__.py
│       ├── levers.py      # Роуты для рычагов
│       └── projects.py    # Роуты для проектов
├── main.py                # Точка входа FastAPI
├── requirements.txt       # Зависимости
├── railway.json          # Конфигурация для Railway
├── runtime.txt           # Версия Python для деплоя
└── README.md             # Документация
```

## Модель данных

Рычаг (Lever) содержит:
- `id`: Уникальный идентификатор
- `name`: Название рычага
- `description`: Описание (опционально)
- `position`: Позиция рычага (0.0 - 100.0)
- `is_active`: Активен ли рычаг
- `created_at`: Дата создания
- `updated_at`: Дата последнего обновления

Проект (Project) содержит:
- `id`: Уникальный идентификатор
- `title`: Название проекта
- `short_description`: Краткое описание
- `full_description`: Полное описание
- `images`: Список ссылок на изображения
- `created_at`: Дата создания записи
- `updated_at`: Дата последнего обновления записи

