__author__ = 'herve'

import os
import os.path
import io
from fabric.api import run
from fabric.api import settings
from fabric.api import cd
from fabric.api import sudo
from fabric.api import put
from fabric.api import env
from fabric.api import prefix

RELEASE_CANDIDATE = True

class Project:
    def __init__(self):
        self.username = raw_input("Server username : ")
        self.password = raw_input("Server password : ")
        self.github = 'https://github.com/4383/street-workout-database.git'
        self.branch = 'master'
        self.domain = 'the-street-workout-database.ovh'
        self.port = 3333
        self.name = 'swd'
        self.path = 'street-workout-database/sport/'
        self.virtualenv = 'virtualenv'
        self.python = 'python3.2'
        self.publish_dependencies_path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)),
            '../',
            'resources'
        )

    def is_initialized(self):
        return self.username is not None

    def home_path(self):
        return "/home/{0}/".format(self.username)

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


def nginx():
    project = Project()
    nginx_template = os.path.join(project.publish_dependencies_path, 'production.swd.conf')
    nginx_file_content = []
    for line in io.open(nginx_template, 'r+'):
        line = line.replace('$site_domain', project.domain)
        line = line.replace('$prefixed_site_domain', project.domain)
        line = line.replace('$gunicorn_port', str(project.port))
        line = line.replace('$media_dir', '/home/{0}/www/{1}/media'.format(project.username, project.name))
        line = line.replace('$static_dir', '/home/{0}/www/{1}/static'.format(project.username, project.name))
        line = line.replace('$static_domain', 'static.{0}'.format(project.domain))
        line = line.replace('$media_domain', 'media.{0}'.format(project.domain))
        nginx_file_content.append(line)

    output_filename = '{0}.conf'.format(project.name)
    output_file_path = os.path.join(project.publish_dependencies_path, output_filename)
    with open(output_file_path, 'w+') as output_file:
        for line in nginx_file_content:
            output_file.write(line)

    put(output_file_path, '/etc/nginx/sites-available')
    run('ln -s /etc/nginx/sites-available/{0} /etc/nginx/sites-enabled'.format(output_filename))
    run('service nginx restart')


def install():
    project = Project()
    env.user = project.username
    env.password = project.password
    #postgres(project)
    with settings(sudo_user=project.username, password=project.password):
        # prepare commands
        create_virtualenv = "{0} --python={2} {1}".format(project.virtualenv, project.install_path(), project.python)
        activate_venv = "source bin/activate"
        clone_project_branch = "git clone -b {0} {1}".format(project.branch, project.github)
        pip_install_requirements = "{1}bin/pip install -r {0}requirements.txt".format(project.full_path(), project.install_path())
        #decrypt_conf = "gpg -d core.txt.gpg >> {0}bin/activate".format(project.install_path())
        # run commands
        run(create_virtualenv)
        with cd(project.install_path()):
            run(activate_venv)
            run(clone_project_branch)
            run(pip_install_requirements)

    nginx(project)
    demonized(project)


def demonized(project=None):
    if not project:
        project = Project()
    service_file = '/etc/init.d/{0}'.format(project.name)
    demon = 'echo "cd {0} && source {0}bin/activate && cd {1} && {0}bin/{3} {0}bin/gunicorn -b 127.0.0.1:3333 sport.wsgi:application &" > {2}'.format(
        project.install_path(),
        project.full_path(),
        service_file,
        project.python
    )
    chmod = 'chmod ugo+x {0}'.format(service_file)
    run(demon)
    run(chmod)


def update():
    project = Project()
    activate = 'source bin/activate'
    collect_static = '{0}bin/{2} {1}manage.py collectstatic'.format(
        project.install_path(),
        project.full_path(),
        project.python
    )
    makemigrations = '{0}bin/{2} {1}manage.py makemigrations'.format(
        project.install_path(),
        project.full_path(),
        project.python
    )
    migrate = '{0}bin/{2} {1}manage.py migrate'.format(
        project.install_path(),
        project.full_path(),
        project.python
    )
    with cd(project.install_path()):
        with prefix(activate):
            run(collect_static)
            run(makemigrations)
            run(migrate)


def start():
    runserver = "sh /etc/init.d/{0}".format(project.name)
    run(runserver)
