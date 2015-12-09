__author__ = 'herve'
#
# Use tmux to continuous monitoring on your server
#
# Monitoring:
# - show databases  : watch -n 20 "psql -l"
# - show roles      : watch -n 20 "psql -c '\du'"
#
# Others:
# - drop database   : su - postgres -c "dropdb <database name>"
# - drop role       : su - postgres -c "psql -c 'DROP USER <username>'"
#

from fabric.api import run
from fabric.api import settings
from fabric.api import sudo


def setup_server():
    run("aptitude install postgresql postgresql-contrib")


def setup_project_database_on_once_environment():
    username = raw_input("Environment name: ")
    project_name = raw_input("Project name: ")
    password = raw_input("Database user password: ")
    database_role = "{0}_{1}".format(username, project_name)
    with settings(sudo_prefix="su - postgres -c "):
        sudo('''psql -c "CREATE USER {0} WITH PASSWORD '{1}';"'''. format(database_role, password))
        sudo('''psql -c "CREATE DATABASE {0}_db;"'''.format(database_role))
        sudo('''psql -c "GRANT ALL PRIVILEGES ON DATABASE {0}_db to {0};"'''.format(database_role))
