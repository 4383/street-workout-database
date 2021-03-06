__author__ = 'herve'

import sys
import md5
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
    run("echo '{0}\n' | adduser {1} --ingroup webuser".format(password, username))
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
        sudo("chown -R {0}:webuser /home/{0}".format(username))
        print("Save and store your private ssh key:")
        print(stdin)


def generate_random_string():
    import random
    available_chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    SECRET_KEY = ''.join([random.SystemRandom().choice(available_chars) for i in range(50)])
    return SECRET_KEY


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
        sudo("mkdir -p /home/{1}/git/{1}.{0}.git".format(project_name, username))
        sudo("mkdir -p /home/{1}/www/{0}/static".format(project_name, username))
        sudo("mkdir -p /home/{1}/www/{0}/media".format(project_name, username))
        sudo("mkdir -p /home/{1}/logs/{0}".format(project_name, username))
        sudo("mkdir -p /home/{1}/sockets/{0}/run".format(project_name, username))
        sudo("touch /home/{0}/sockets/{1}/run/gunicorn.sock".format(username, project_name))
        sudo("virtualenv-3.2 /home/{1}/projects/{0}".format(project_name, username))

        secret_key = generate_random_string()

        password = md5.new()
        password.update(secret_key)

        print(secret_key)
        sudo('''echo 'export SECRET_KEY="{2}"' >> /home/{1}/projects/{0}/bin/activate'''.format(
            project_name,
            username,
            secret_key
        ))
        sudo('''echo 'export DATABASE_DEFAULT_USER="{1}_{0}"' >> /home/{1}/projects/{0}/bin/activate'''.format(
            project_name,
            username,
        ))
        sudo('''echo 'export DATABASE_DEFAULT_PASSWORD="{2}"' >> /home/{1}/projects/{0}/bin/activate'''.format(
            project_name,
            username,
            password.hexdigest()
        ))
        with cd("/home/{1}/git/{1}.{0}.git".format(project_name, username)):
            sudo("git init --bare")

        sudo("chown -R {0}:webuser /home/{0}".format(username))
