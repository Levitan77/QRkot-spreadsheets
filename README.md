# QRkot-spreadsheets

## Описание

Проект представляет из себя бэкенд приложения для создания благотворительных проектов и пожертвований
Реализована автоматическая система инвестирования пожертвований в проекты

### Основной функционал

- Регистрация и авторизация пользователей
- Создание проекта админом
- Создание именного пожертвования
- Изменение проекта админов
- Распределение финансов по проектам
- Создание отчетов в гугл таблицах

## Cтек использованных технологий

- Python 3.10
- alembic==1.7.7
- fastapi==0.111.0
- SQLite/PostgreSQL
- pydantic==2.7.1
- SQLAlchemy==2.0.29
- aiogoogle==5.13.0


## Установка

Для установки и запуска проекта выполните следующие действия:

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone
cd QRkot-spreadsheets/
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать в директории проекта файл .env с переменными окружения:

```
APP_TITLE=Cat Charity
DATABASE_URL=sqlite+aiosqlite:///./cat_charity.db
SECRET=veryverysecret

TYPE=тип аккаунта
PROJECT_ID=id проекта
PRIVATE_KEY_ID=id приватного ключа
PRIVATE_KEY=приватный ключ
CLIENT_EMAIL=email сервисного аккаунта
CLIENT_ID=id сервисного аккаунта
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=url
EMAIL=email
```

Создать базу данных и применить миграции:

```
alembic upgrade head
```

Запустить проект:

```
uvicorn app.main:app --reload
```

## Примеры работы Api запросов

### Создание пожертвования

Запрос:

```
URL: http://127.0.0.1:8000/donation/
Method: POST

{
    "full_amount": 100
}
```

Ответ:

```
Status Code: 201 Created

{
    "invested_amount": 0,
    "fully_invested": false,
    "close_date": None,
    "create_date": "2026-11-16T12:23:41.095367Z",
    "id": 1
}
```

### Просмотр списка проектов

Запрос:

```
URL: http://127.0.0.1:8000/charity_project/
Method: GET
```

Ответ:

```
Status Code: 200 OK

[
    {
        "id": 1,
        "invested_amount": 2000,
        "fully_invested": false,
        "full_amount": 3000,
        "name": "name",
        "create_date": "2026-11-16T12:23:41.095367Z",
        "close_date": None
    }
]
```


## Автор

[Levitan77](https://github.com/Levitan77)