# manage.py
import os

from flask.ext.script import Manager, Shell, Server
from flask.ext.security import MongoEngineUserDatastore
from flask.ext.security.utils import encrypt_password

from ulti import create_app
from ulti.config import ProductionConfig, DevelopmentConfig
from ulti.extensions import db
from ulti.user import User, Role

if os.environ.get('PRODUCTION'):
    app = create_app(config = ProductionConfig)
else:
    app = create_app()

manager = Manager(app)

@manager.command
def initdb():
    '''Init/reset database.'''
    if not os.environ.get('PRODUCTION'):
        db.connection.drop_database(app.config['MONGODB_DB'])

    user_datastore = MongoEngineUserDatastore(db, User, Role)

    admin_role = user_datastore.create_role(name='super_admin', description='Super Admin')
    team_role = user_datastore.create_role(name='team_admin', description='Team Admin')
    user = user_datastore.create_user(
        email='joe.a.hand@gmail.com',
        password=encrypt_password('password')
    )

    user_datastore.add_role_to_user(user, admin_role)

@manager.command
def buildjs():
    ''' Builds the js for production
        TODO: Build css here too.
    '''
    jsfile = 'app.min.js'
    os.system('cd ulti/static/js && node libs/r.js -o app.build.js out=../build/%s'%jsfile)
    os.system('cd ulti/static/js && cp libs/require.js ../build/')
    jsfile = 'ulti/static/build/' + jsfile

def shell_context():
    return dict(app=app)

#runs the app
if __name__ == '__main__':
    manager.add_command('shell', Shell(make_context=shell_context))
    manager.run()
