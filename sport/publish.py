__author__ = 'herve'

import os
import os.path
from fabric.api import run
from fabric.api import settings
from fabric.api import cd
from fabric.api import sudo


class Project:
    def __init__(self):
        self.username = input("Server username : ")
        self.password = input("Server password : ")
        self.github = 'https://github.com/4383/street-workout-database.git'
        self.branch = 'prodV0'
        self.domain = 'the-street-workout-database.ovh'
        self.port = 666
        self.name = 'swd'
        self.path = 'street-workout-database/sport/'
        self.static_path = '{0}static/'.format(self.path)
        self.media_path = '{0}media/'.format(self.path)
        self.virtualenv = 'virtualenv-3.2'
        self.publish_dependencies_path = os.path.dirname(os.path.dirname(__file__))

    def is_initialized(self):
        return self.server_username is not None

    def home_path(self):
        return "/home/{0}/".format(self.server_username)

    def install_path(self):
        return "{0}{1}/".format(self.home_path(), self.name)

    def full_path(self):
        return "{0}{1}".format(self.install_path(), self.path)


def postgres(project):
    commands = [
        '''psql -c "CREATE USER {0} WITH PASSWORD '{1}';"''' . format(project.username, project.password),
        '''psql -c "CREATE DATABASE db{0};"''' . format(project.username),
        '''psql -c "GRANT ALL PRIVILEGES ON DATABASE db{0} to {0};"''' . format(project.username)
    ]

    for command in commands:
        sudo(command, user='postgres')


def nginx(project):
    nginx_template = os.path.join(project.publish_dependencies_path, 'nginx.conf')
    nginx_file_content = []
    with open(nginx_template, 'r+') as template:
        for line in template.readlines():
            line = line.replace('$site_domain', project.domain)
            line = line.replace('$gunicorn_port', project.port)
            nginx_file_content.append(line)

    output_filename = '{0}.conf'.format(project.name)
    with open(os.path.join(project.publish_dependencies_path, output_filename), 'w+') as output_file:
        for line in nginx_file_content:
            output_file.write(line)

def install():
    project = Project()
    with settings(sudo_user=project.username, password=project.password):
        # prepare commands
        create_virtualenv = "{0} {1}".format(project.virtualenv, project.install_path())
        activate_venv = "source bin/activate".format(project.install_path())
        clone_project_branch = "git clone -b {0} {1}".format(project.branch, project.github)
        pip_install_requirements = "pip install -r {0}requirements.txt".format(project.full_path())
        # run commands
        run(create_virtualenv)
        with cd(project.install_path()):
            run(activate_venv)
            run(clone_project_branch)
            run(pip_install_requirements)

    postgres(project)


def update():
    pass


def restart():
    pass


def stop():
    pass


def start():
    pass
