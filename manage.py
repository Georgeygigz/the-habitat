from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from api.models.databases import db
from api.models.auth_modles import User
from api.models.products_model import Products

from instance.config import AppConfig
app = create_app(AppConfig)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()