from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app.bucketlist.models import db
from run import app
import os
basedir = os.path.abspath(os.path.dirname(__file__))

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
