__author__ = 'herve'

import os
import os.path
from fabric.api import run
from fabric.api import settings
from fabric.api import cd
from fabric.api import sudo
from fabric.api import put
from fabric.api import env


class Project:
    def __init__(self):
        self.username = raw_input("Server username : ")
        self.password = raw_input("Server password : ")
        self.github = 'https://github.com/4383/street-workout-database.git'
        self.branch = 'prodV0'
        self.domain = 'the-street-workout-database.ovh'
        self.port = 666
        self.name = 'swd'
        self.path = 'street-workout-database/sport/'
        self.static_path = '{0}static/'.format(self.path)
        self.media_path = '{0}media/'.format(self.path)
        self.virtualenv = 'virtualenv'
        self.publish_dependencies_path = os.path.dirname(os.path.dirname(__file__))

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


def nginx(project):
    nginx_template = os.path.join(project.publish_dependencies_path, 'nginx.conf')
    nginx_file_content = []
    with open(nginx_template, 'r+') as template:
        for line in template.readlines():
            line = line.replace('$site_domain', project.domain)
            line = line.replace('$gunicorn_port', project.port)
            line = line.replace('$path_site', project.full_path())
            nginx_file_content.append(line)

    output_filename = '{0}.conf'.format(project.name)
    output_file_path = os.path.join(project.publish_dependencies_path, output_filename)
    with open(output_file_path, 'w+') as output_file:
        for line in nginx_file_content:
            output_file.write(line)

    put(output_file_path, '/etc/nginx/site-available')
    run('ln -s /etc/nginx/site-available/{0} /etc/nginx/site-enabled'.format(output_filename))
    run('service nginx restart')


def install():
    project = Project()
    env.user = project.username
    env.password = project.password
    #postgres(project)
    with settings(sudo_user=project.username, password=project.password):
        # prepare commands
        create_virtualenv = "{0} --python=python2.7 {1}".format(project.virtualenv, project.install_path())
        activate_venv = "source bin/activate".format(project.install_path())
        clone_project_branch = "git clone -b {0} {1}".format(project.branch, project.github)
        pip_install_requirements = "{1}bin/pip install -r {0}requirements.txt".format(project.full_path(), project.install_path())
        decrypt_conf = "gpg -d core.txt.gpg >> {0}bin/activate".format(project.install_path())
        # run commands
        run(create_virtualenv)
        with cd(project.install_path()):
            run(activate_venv)
            run(clone_project_branch)
            run(pip_install_requirements)
            run(decrypt_conf)

        start(project)
    nginx(project)


def update():
    project = Project()
    with settings(sudo_user=project.username, password=project.password):
        with cd(project.install_path()):
            run("git pull origin {0}".format(project.branch))

        start(project)

def restart():
    pass


def stop():
    pass


#def is_already_running(project):
#    if project.port in gunicorn_instances():
#        return True
#    return False


#def gunicorn_instances():
#    instances = run('ps ax | grep gunicorn | grep -v grep')
#    return instances


#def pids(project):
#    pids_list = []
#    for instance in gunicorn_instances():
#        if project.port in instance:
#            pids_list.append(instance.split(' ')[0])


def start(project):
    #if is_already_running(project):
    #    print("This project is already running")
    start_gunicorn = "{1}bin/python ../../bin/gunicorn -b 127.0.0.1:{0} sport.wsgi:application".format(project.port, project.install_path())
    with cd(project.full_path()):
        run("python manage.py collectstatic")
        run(start_gunicorn)
