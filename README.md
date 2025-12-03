Установка Alembic
```
pip install alembic
```
Создание Файлов и Папки для Миграции
```
alembic init <название папки>
```
У нас появился файл alembic.ini
Отвечает за конфигурацию базы данных
```
pip install psycopg2
```
psycopg2 - помогает нам работать с Postgres драйвер
Он синхронный

В alembic.ini мы изменили значение переменной sqlalchemy.url
sqlalchemy.url = postgresql+psycopg2://postgres:1234@localhost:5432/DeliveryBot

* postgresql+psycopg2 -> Отвечает за то что какая СУБД
* postgres:1234 -> юзернейм:пароль к БД
* localhost:5432 -> Хост на котором наша БД и порт 
* DeliveryBot -> название БД

Мы открыли папку миграций и внутри env.py

в Котором мы прописали 

from models.base import Base
from models.category import Category
from models.product import Product
from models.order import Order, OrderProduct
from models.user import User

target_metadata = Base.metadata

Создание Миграции
```shell
alembic revision --autogenerate -m "Название Миграции" 
```
* --autogenerate -> Позволяет автоматически брать изменении БД
* -m -> Название для нашей версии

Применение Миграции
```shell
alembic upgrade <версия миграции>
```
Применение Всех версий Миграции
```shell
alembic upgrade head
```

Откатиться на Пред Версию
```shell
alembic downgrade -1
```
Откатиться на Определенную Версию
```shell
alembic downgrade <версия миграции>
```