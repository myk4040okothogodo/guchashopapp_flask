from flask_script import Manager, prompt_bool, Shell, Server
from termcolor import colored
from app import app, db, models
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app, db=db)

@manager.command
def initdb():
    """ create the SQL database."""
    db.create_all()
    print(colored('The SQL database has been created','green'))


@manager.command
def dropdb():
    """Delete the SQL database."""
    if prompt_bool('Are you sure u want to delete all the SQL data.?'):
        db.drop_all()
        print(colored('The SQL database has been deleted', 'red'))
    else:
        print(colored('Database not deleted', 'green'))


manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
