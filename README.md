Установка alembic
'''
pip install alembic
'''
создание файлов и папки для миграции 
'''
alembic init<название папки>
'''
у нас появился alembic.ini
отвечает за конфигурацию базы данных
'''
pip install psycopg2
'''
psycopg2 - помогает нам работать с Постргрес драверами 
он синхронный 

В alembic.ini мы изменили изменили значение переменной sqlalchemy.url
sqlalchemy.url = postgresql+psycopg2://postgres:1@localhost:5432/DeliveryBot

* postgresql+psycopg2 -> отвечает за то что какая СУБД
* postgres:1 -> username:пароль к БД
* localhost:5432 -> Хост на котором наша БД и порт
* DeliveryBot -> название БД 


from models.base import Base
from models.category import Category
from models.product import Product
from models.order import Order,OrderProduct
from models.user import User

target_metadata = Base.metadata

создание миграции 
'''
alembic revision --autogenerate -m "название Миграции"
'''
--autogenerate -> Позволяет автоматически брать изменения

применение миграции 
'''
alembic upgrade <version of migration>
'''
'''
alembic upgrade head
'''

откатится на пред версию
'''
alembic downgrade -1
'''
откатится на опред версию
'''
alembic downgrade <версия миграции>
'''