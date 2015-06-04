from StringIO import StringIO

from fabric import api
from fabric.contrib.files import exists


# UPSTART_TEMPLATE = """
# description "Pi-System-RPC-Service"
# start on runlevel [2345]
# stop on runlevel [06]
# respawn
# respawn limit 10 5
# env LOGGLY_TOKEN={loggly_token}
# env LOGGLY_SUBDOMAIN={loggly_domain}
# env RABBIT_URL={rabbit_url}
# script
#         cd /home/pi/Pi-System-RPC-Service/app && node main.js
# end script
# """

UPSTART_FILE_NAME = 'pi-thpl-reporter.conf'
UPSTART_FILE_PATH = '/etc/init/{0}'.format(UPSTART_FILE_NAME)
UPSTART_SERVICE_NAME = UPSTART_FILE_NAME.split('.')[0]
GITHUB_REPO = 'https://github.com/projectweekend/Pi-DynamoDB-Reporter.git'
LOCAL_REPO_NAME = UPSTART_FILE_NAME
LOCAL_REPO_PATH = '~/{0}'.format(LOCAL_REPO_NAME)
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
    upstart_values['project_description'] = api.prompt('Project description:')
    upstart_values['loggly_token'] = api.prompt('Loggly token:')
    upstart_values['loggly_domain'] = api.prompt('Loggly domain:')
    upstart_values['rabbit_url'] = api.prompt('Rabbit URL:')
    upstart_file = StringIO(UPSTART_TEMPLATE.format(**upstart_values))

    api.sudo('echo Yes, do as I say! | apt-get -y --force-yes install upstart')

    with api.cd('/etc/init'):
        upload = api.put(upstart_file, UPSTART_FILE_NAME, use_sudo=True)
        assert upload.succeeded

    api.run('git clone {0} {1}'.format(GITHUB_REPO, LOCAL_REPO_NAME))

    with api.cd(LOCAL_REPO_PATH):
        api.sudo(INSTALL_DEPENDENCIES)

    api.sudo(START_SERVICE)


def update():
    api.require('hosts', provided_by=[raspberry_pi])

    with api.settings(warn_only=True):
        api.sudo(STOP_SERVICE)

    with api.cd(LOCAL_REPO_PATH):
        api.run('git pull origin master')
        api.sudo(INSTALL_DEPENDENCIES)

    api.sudo(START_SERVICE)
