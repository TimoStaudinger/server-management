from fabric.api import sudo, run, task, env, settings, cd, put
from fabric.contrib.files import sed
from config import USER, PUBLIC_KEY_FILE

@task
def root_setup():
    env.user = 'root'

    sudo('adduser {} --gecos ""'.format(USER))
    sudo('usermod -aG sudo {}'.format(USER))

    sed('/etc/ssh/sshd_config', 'PermitRootLogon yes', 'PermitRootLogon no')

    with settings(user=USER):
        run('mkdir ~/.ssh')
        run('chmod 700 ~/.ssh')

        put(PUBLIC_KEY_FILE, '~/.ssh/id_rsa.pub', mode=0600)
        run('cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys')

    sudo('service ssh restart')

@task
def jre_setup():
    sudo('apt-get update')
    sudo('apt-get install openjdk-8-jre')

@task
def update():
    sudo("apt-get update")
    sudo("apt-get upgrade -y")
