#!/usr/bin/env python
import os

if os.path.exists('.env'):
    print('Importing environment from .env ...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# Configure an app manager
app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """Import key instances for shell debugging"""
    return dict(app=app, db=db, User=User, Role=Role)


# Add commands to the application manager
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import Role, User

    # Upgrade the database
    upgrade()

    # Create user roles
    Role.insert_roles()


if __name__ == '__main__':
    manager.run()
