__author__ = 'herve'

import sys
from fabric.api import run
from fabric.api import settings
from fabric.api import cd
from fabric.api import sudo
from fabric.api import env


def root_is_required(func):
    """
    Functionality require an root access (user)
    """
    if env.user != 'root':
        print('Function require root user !')
        sys.exit(1)
    return func


@root_is_required
def setup_server_for_projects_workflow_instance():
    """
    Create and configure new user on your.
    You can use this account for deploy
    django project with best-practices
    :return:
    """
    username = raw_input("Username to create on server: ")
    password = raw_input("User password: ")
    run("echo '{0}\n' | adduser {1}".format(password, username))
    with settings(
            password=password,
            sudo_prefix="su {0} -c ".format(username),
    ):
        sudo("mkdir -p /home/{0}/www".format(username))
        sudo("mkdir -p /home/{0}/git".format(username))
        sudo("mkdir -p /home/{0}/logs".format(username))
        sudo("mkdir -p /home/{0}/projects".format(username))
        sudo("mkdir -p /home/{0}/sockets".format(username))
        sudo("mkdir -p /home/{0}/.ssh".format(username))
        sudo("echo '' | ssh-keygen")
        sudo("cat /home/{0}/.ssh/id_rsa.pub >> /home/{0}/.ssh/authorized_keys".format(username))
        stdin = sudo("cat /home/{0}/.ssh/id_rsa".format(username))
        print("Save and store your private ssh key:")
        print(stdin)


@root_is_required
def setup_project_environment():
    """
    Prepare new project hosting on specified user account
    on specified servers.
    Deploy your project with git-deploy
    :return:
    """
    username = raw_input("Username to use on server: ")
    password = raw_input("User password: ")
    project_name = raw_input("Enter your project name: ")
    with settings(
            password=password,
            sudo_prefix="su {0} -c ".format(username),
    ):
        run("mkdir -p /home/{1}/git/{0}.{1}.git".format(project_name, username))
        run("mkdir -p /home/{1}/www/{0}/static".format(project_name, username))
        run("mkdir -p /home/{1}/www/{0}/media".format(project_name, username))
        run("mkdir -p /home/{1}/logs/{0}".format(project_name, username))
        run("mkdir -p /home/{1}/sockets/{0}/run".format(project_name, username))
        run("virtualenv-3.2 /home/{1}/projects/{0}".format(project_name, username))
        with cd("/home/{1}/git/{0}.git".format(project_name, username)):
            run("git init --bare")
