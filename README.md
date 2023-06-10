# Домашнє завдання #7

Робота з базою [`MongoDB`](https://www.mongodb.com/)[^1] за допомогою [`ODM MongoEngine`](https://docs.mongoengine.org/)[^2].

[^1]: `документо-орієнтована система керування базами даних (СКБД) з відкритим вихідним кодом, яка не потребує опису схеми таблиць. MongoDB займає нішу між швидкими і масштабованими системами, що оперують даними у форматі ключ/значення, і реляційними СКБД, функціональними і зручними у формуванні запитів.

[^2]: `MongoEngine` - це об'єктно-документний маппер (Object-Document Mapper), написаний на Python для роботи з MongoDB.

## Установка і запуск проекту

Для управління залежностями проекту використовується `pipenv`. Необхідно встановити `pipenv` перед виконанням наступних кроків:

- Склонируйте репозиторий:

  ```shell
  git clone https://github.com/sergiokapone/goit_python_web_hw8_1_.git
  ```

- Для встановлення залежностей використайте команду `pipenv install` або `pipenv sync`.

- Для зручності запуску проекту на `Winows` можна запустити файл `project_run.cmd`

## Сртуктура проекту

```text
.
├── database/
│   ├── connect.py          # Код для керування підключенням до бази даних
│   └──  models.py          # Визначення моделей даних
├── Pipfile
├── alembic_run_.cmd        # Робота з міграціями
├── config.ini              # Налаштування для підключення до бази даних
├── README.MD
├── upload.py               # Код для заповнення бази даних початковими даними
└── query.py                # Код виконання запитів до бази даних
```

## Заповнення бази даних

Для заповнення бази даних можна скористатись командою `python upload.py`. Файл `upload.py`
містить сценарій для завантаження данних з файлів `authors.json` та `quotes.json` до бази данних.

## Запити до бази данних

`query.py` є інтерфейсом командного рядка (CLI). який дає змогу взаємодіяти з базою даних студентів із командного рядка.

### Приклади виконання команд у терміналі.


