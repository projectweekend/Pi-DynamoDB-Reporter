from StringIO import StringIO

from fabric import api
from fabric.contrib.files import exists


UPSTART_TEMPLATE = """
description "Temperature, Humidity, Pressure, & Luminosity Reporter"
start on runlevel [2345]
stop on runlevel [06]
respawn
respawn limit 10 5
env AWS_ACCESS_KEY_ID={aws_access_key_id}
env AWS_SECRET_ACCESS_KEY={aws_secret_access_key}
script
        cd /opt/{local_repo_name} && sudo -E python main.py
end script
"""

UPSTART_FILE_NAME = 'pi-thpl-reporter.conf'
UPSTART_DIRECTORY = '/etc/init'
UPSTART_FILE_PATH = '{0}/{1}'.format(UPSTART_DIRECTORY, UPSTART_FILE_NAME)
UPSTART_SERVICE_NAME = UPSTART_FILE_NAME.split('.')[0]
REMOTE_REPO = 'https://github.com/projectweekend/Pi-DynamoDB-Reporter.git'
LOCAL_INSTALL_DIRECTORY = '/opt'
LOCAL_REPO_NAME = UPSTART_SERVICE_NAME
LOCAL_REPO_PATH = '{0}/{1}'.format(LOCAL_INSTALL_DIRECTORY, LOCAL_REPO_NAME)
START_SERVICE = 'service {0} start'.format(UPSTART_SERVICE_NAME)
STOP_SERVICE = 'service {0} stop'.format(UPSTART_SERVICE_NAME)
INSTALL_DEPENDENCIES = 'pip install -r requirements.txt'


def raspberry_pi():
    api.env.hosts = ['{0}.local'.format(api.prompt('RPi Hostname:'))]
    api.env.user = 'pi'


def install():
    api.require('hosts', provided_by=[raspberry_pi])

    if exists(UPSTART_FILE_PATH, use_sudo=True):
        print('"{0}" is already installed, use "update" to deploy changes'.format(UPSTART_SERVICE_NAME))
        return

    upstart_values = {}
    upstart_values['aws_access_key_id'] = api.prompt('AWS_ACCESS_KEY_ID:')
    upstart_values['aws_secret_access_key'] = api.prompt('AWS_SECRET_ACCESS_KEY:')
    upstart_values['local_repo_name'] = LOCAL_REPO_NAME
    upstart_file = StringIO(UPSTART_TEMPLATE.format(**upstart_values))

    api.sudo('echo Yes, do as I say! | apt-get -y --force-yes install upstart')

    with api.cd(UPSTART_DIRECTORY):
        upload = api.put(upstart_file, UPSTART_FILE_NAME, use_sudo=True)
        assert upload.succeeded

    with api.cd(LOCAL_INSTALL_DIRECTORY):
        api.sudo('git clone {0} {1}'.format(REMOTE_REPO, LOCAL_REPO_NAME))

    with api.cd(LOCAL_REPO_PATH):
        api.sudo(INSTALL_DEPENDENCIES)

    api.sudo(START_SERVICE)


def update():
    api.require('hosts', provided_by=[raspberry_pi])

    with api.settings(warn_only=True):
        api.sudo(STOP_SERVICE)

    with api.cd(LOCAL_REPO_PATH):
        api.sudo('git pull origin master')
        api.sudo(INSTALL_DEPENDENCIES)

    api.sudo(START_SERVICE)
