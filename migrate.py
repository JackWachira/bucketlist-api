from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from models import db, app


migrate = Migrate(app, db, "/migrations")

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
