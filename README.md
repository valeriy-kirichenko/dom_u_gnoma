# dom_u_gnoma :house_with_garden:
Сайт рукодельных изделий (по ходу написания проекта буду добавлять описание).
Сайт пока без дизайна, это в последнюю очередь. Пока все страшненько и некрасивенько, со временем буду дорабатывать "напильником" так сказать :smiley:

Реализована регистрация пользователей с активацией через электронную почту.
Активация реализована с помощью сигналов Django.

Есть страница с каталогом изделий, страница с отдельным изделием где указана его цена и описание.

# Установка
Системные требования
----------
* Python 3.7+
* Works on Linux, Windows, macOS

Стек технологий
----------
* [Python >=3.7](https://www.python.org/downloads/)
* Django 4.1.3
* SQLite3
* [Poetry 1.2.2](https://python-poetry.org/docs/#installation)
* [Git](https://git-scm.com/downloads)


Установка проекта из репозитория (Windows)
----------
1. Клонируйте репозиторий и перейдите в него в командной строке:
```bash
git clone 'git@github.com:valeriy-kirichenko/dom_u_gnoma.git'
cd dom_u_gnoma/ # перейдите в папку с проектом
```

2. Установите необходимые пакеты:
```bash
# имеется ввиду что у вас уже установлены pip и poetry(ссылка в пункте "Стек технологий")

poetry shell # активирует виртуальное окружение
poetry install # устанавливает пакеты из poetry.lock

# либо можно установить пакеты с помощью стандартного менеджера пакетов
python -m venv venv # устанавливает виртуальное окружение
source venv/Scripts/activate # активирует виртуальное окружение
pip install -r requirements.txt # устанавливает пакеты из requirements.txt
```

3. Запустите проект:
```bash
python dom_u_gnoma/manage.py runserver
```
----------
Автор:
----------
* **Кириченко Валерий Михайлович**
GitHub - [valeriy-kirichenko](https://github.com/valeriy-kirichenko)
